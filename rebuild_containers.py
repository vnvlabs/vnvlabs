import json

import docker
import hashlib
import subprocess
import os
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description='Description of your script')

# Add the arguments
parser.add_argument('--repo_owner', type=str, help='The owner of the container registry', default='ghcr.io/vnvlabs')
parser.add_argument('--tag', type=str, help='The version or branch of code to use', default='nightly')
parser.add_argument('--ref_tag', type=str, help='The reference tag', default='nightly')
parser.add_argument('--full_rebuild', action='store_true', help='Whether to perform a full rebuild')
parser.add_argument('--actually_build', action='store_false', help='Whether to actually build the image')
parser.add_argument('--cache_from_nightly', action='store_false', help='Whether to use nightly cache to build')
parser.add_argument('--push', action='store_true', help='Push at end')

# Parse the arguments
args = parser.parse_args()

# Access the values of the arguments
REPO_OWNER = args.repo_owner
TAG = args.tag
REFTAG = args.ref_tag
FULLREBUILD = args.full_rebuild
ACTUALLY_BUILD = args.actually_build
CACHE_FROM_NIGHTLY = args.cache_from_nightly
PUSH_TO_GHCR = args.push

REBUILD_INFO = {}
docker_client = docker.from_env()
docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')


def repo_name(name, repo=REPO_OWNER):
    return f"{repo}/{name}"


def get_git_revision_hash(directory):
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory).decode('ascii').strip()


def get_git_submodule_hash(directory):
    return subprocess.check_output(['git', 'submodule', "status", directory]).decode('ascii')


def init_and_update_submodule(path):
    return subprocess.check_output(["git", "submodule", "update", "--init", "--recursive", path]).decode('ascii')


# Get a hash for a file
def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()


def get_image(image):
    try:
        return docker_client.images.get(image)
    except Exception as e:
        return None


def pull_image(image, tag=TAG):
    try:
        return docker_client.images.pull(image, tag=tag)
    except Exception as e:
        return None


def push_image(image, tag=TAG):
    try:
        docker_client.images.push(image, tag=tag)
    except Exception as e:
        return None


def build_image(build_context, dockerfile_rel_bc, cache_from, repo_and_tag, build_args, labels):
    for c in cache_from:
        a = c.split(":")
        pull_image(a[0], tag=a[1])

    generator = docker_client.api.build(path=build_context,
                                        dockerfile=dockerfile_rel_bc,
                                        tag=repo_and_tag,
                                        buildargs=build_args,
                                        decode=True,
                                        labels=labels)

    success = False
    logs = []
    while True:
        try:
            output = generator.__next__()
            if 'stream' in output:
                logs.append(output["stream"].strip())
            elif "error" in output:
                for i in logs:
                    print(i)
                print(output["error"])
                success = False
                break
        except StopIteration:
            success = True
            print("Docker image build complete.")
            break
        except ValueError:
            print("Error parsing output from docker image build: %s" % output)
            success = False

    return success


def file_needs_rebuild(path, reponame, tag=REFTAG, repo=REPO_OWNER, from_image=None, otag=TAG, ftag=TAG, build_args={},
                       dependencies=[]):
    # Step 1a Check if we need to build env
    REBUILD = True
    REBUILD_SHA = sha256sum(path)

    if FULLREBUILD is False:
        if from_image is None or REBUILD_INFO[from_image][0] is False:
            if True not in [REBUILD_INFO[a][0] for a in dependencies]:  # And none of the other deps were modified
                image = pull_image(repo_name(reponame, repo=repo), tag=tag)
                if image is not None and "vnvsha" in image.labels:
                    if image.labels["vnvsha"] == REBUILD_SHA:
                        REBUILD = False
                    else:
                        print("Rebuilding because repo commit changed ", image.labels["vnvsha"], REBUILD_SHA)
                elif image is None:
                    print("Rebuilding because nightly image ", f"{repo_name(reponame, repo=repo)}:{otag}", " is none")
                else:
                    print("Rebuilding because vnvsha not in nightly image")
            else:
                print("Rebuilding because one of the dependencies is rebuilt:",
                      [a for a in REBUILD_INFO.keys() if REBUILD_INFO[a][0]])
        else:
            print("Rebuilding because ", from_image, " was rebuilt")
    else:
        print("Rebuilding because full_rebuild was requested")
    rname = reponame
    if reponame in REBUILD_INFO:
        rname = "f" + reponame

    REBUILD_INFO[rname] = [REBUILD, REBUILD_SHA]

    if ACTUALLY_BUILD:

        if from_image is not None and REBUILD_INFO[from_image][2] is False:
            print("Skipping Build because from_image failed")
            REBUILD_INFO[rname].append(False)
            return

        for i in dependencies:
            if REBUILD_INFO[i][2] is False:
                print("Skipping build because dependency ", i, " failed")
                REBUILD_INFO[rname].append(False)
                return

        if REBUILD:

            print("Building: ", f"{repo_name(reponame, repo=repo)}:{otag}")

            if from_image is not None:
                build_args["FROM_IMAGE"] = f"{repo_name(from_image, repo=repo)}:{ftag}"

            REBUILD_INFO[rname].append(build_image(
                build_context=os.path.dirname(path),
                dockerfile_rel_bc=os.path.basename(path),
                build_args=build_args,
                cache_from=[] if not CACHE_FROM_NIGHTLY else [f"{repo_name(reponame, repo=repo)}:{tag}"],
                repo_and_tag=f"{repo_name(reponame, repo=repo)}:{otag}",
                labels={"vnvsha": REBUILD_SHA}
            ))

        else:
            print("Skipping Build and Tagging: ", f"{repo_name(reponame, repo=repo)}:{otag}")
            rname1 = f"{repo_name(reponame, repo=repo)}:{tag}"
            docker_client.api.tag(image=rname1, repository=repo_name(reponame, repo=repo), tag=otag)
            REBUILD_INFO[rname].append(True)
    else:
        REBUILD_INFO[rname].append(True)


def repo_needs_rebuild(path, reponame, tag=REFTAG, repo=REPO_OWNER, from_image=None, dockerfile="docker/Dockerfile",
                       otag=TAG, ftag=TAG, build_args={}, dependencies=[]):
    # Step 3: Check if we need to rebuild the gui
    REBUILD = True
    # REBUILD_SHA = get_git_revision_hash(os.path.abspath(path))
    REBUILD_SHA_TEMP = get_git_submodule_hash(path)
    REBUILD_SHA = REBUILD_SHA_TEMP[1:41]
    SUBMODULE_PULL = (REBUILD_SHA_TEMP[0] == "-")

    # Check to see if we can skip rebuild. Cant skip if any of deps are rebuilt.
    try:
        if FULLREBUILD is False:  # If we didnt request a full rebuild
            if from_image is None or REBUILD_INFO[from_image][0] is False:  # and the from_image was not modified
                if True not in [REBUILD_INFO[a][0] for a in dependencies]:  # And none of the other deps were modified
                    nightly = pull_image(repo_name(reponame, repo=repo), tag=tag)
                    if nightly is not None and "vnvsha" in nightly.labels:  # If the docker file has not been modified
                        if nightly.labels["vnvsha"] == REBUILD_SHA:
                            REBUILD = False  # then we dont need to rebuild cause all of the deps have not changed.
                        else:
                            print("Rebuilding because repo commit changed ", nightly.labels["vnvsha"], REBUILD_SHA)
                    elif nightly is None:
                        print("Rebuilding because nightly image ", f"{repo_name(reponame, repo=repo)}:{tag}",
                              " is none")
                    else:
                        print("Rebuilding because vnvsha not in nightly image")
                else:
                    print("Rebuilding because one of the dependencies is rebuilt:",
                          [a for a in REBUILD_INFO.keys() if REBUILD_INFO[a][0]])
            else:
                print("Rebuilding because ", from_image, " was rebuilt")
        else:
            print("Rebuilding because full_rebuild was requested")
    except Exception as e:
        print("Re Building because error found ", e)

    rname = reponame
    if reponame in REBUILD_INFO:
        rname = "f" + reponame

    REBUILD_INFO[rname] = [REBUILD, REBUILD_SHA]

    if ACTUALLY_BUILD:

        if from_image is not None and REBUILD_INFO[from_image][2] is False:
            print("Skipping Build because from_image failed")
            REBUILD_INFO[rname].append(False)
            return

        for i in dependencies:
            if REBUILD_INFO[i][2] is False:
                print("Skipping build because dependency ", i, " failed")
                REBUILD_INFO[rname].append(False)
                return

        if REBUILD:
            print("Building ", f"{repo_name(reponame, repo=repo)}:{otag}")
            if from_image is not None:
                build_args["FROM_IMAGE"] = f"{repo_name(from_image, repo=repo)}:{ftag}"

            if SUBMODULE_PULL:
                init_and_update_submodule(path)

            REBUILD_INFO[rname].append(build_image(
                build_context=path,
                dockerfile_rel_bc=dockerfile,
                build_args=build_args,
                cache_from=[] if not CACHE_FROM_NIGHTLY else [f"{repo_name(reponame, repo=repo)}:{tag}"],
                repo_and_tag=f"{repo_name(reponame, repo=repo)}:{otag}",
                labels={"vnvsha": REBUILD_SHA}
            ))
        else:
            print("Skipping Build and Tagging: ", f"{repo_name(reponame, repo=repo)}:{otag}")
            rname1 = f"{repo_name(reponame, repo=repo)}:{tag}"
            docker_client.api.tag(image=rname1, repository=repo_name(reponame, repo=repo), tag=otag)
            REBUILD_INFO[rname].append(True)
    else:
        REBUILD_INFO[rname].append(True)


# Step 1a Check if we need to build env
file_needs_rebuild("env/Dockerfile", "env")
repo_needs_rebuild("gui", "gui", from_image=None)
repo_needs_rebuild("vnv", "vnv", from_image="env")
repo_needs_rebuild("plugins/performance", "performance", from_image="vnv")
repo_needs_rebuild("applications/asgard", "asgard", from_image="vnv")
repo_needs_rebuild("applications/heat", "heat", from_image="vnv")
repo_needs_rebuild("applications/simple", "simple", from_image="vnv")
repo_needs_rebuild("applications/miniamr", "miniamr", from_image="vnv")
repo_needs_rebuild("applications/swfft", "swfft", from_image="vnv")
repo_needs_rebuild("applications/xsbench", "xsbench", from_image="vnv")
repo_needs_rebuild("applications/hypre", "hypre", from_image="vnv")
repo_needs_rebuild("applications/petsc", "petsc", from_image="hypre")
repo_needs_rebuild("applications/libmesh", "libmesh", from_image="petsc")
repo_needs_rebuild("applications/mfem", "mfem", from_image="petsc")
repo_needs_rebuild("applications/moose", "moose", from_image="libmesh")

# Look at some multistage builds:
build_args = {"VERSION": TAG, "REPO": REPO_OWNER}
file_needs_rebuild("applications/docker/Dockerfile_demo", "demo", dependencies=["simple", "heat"],
                   build_args=build_args)
file_needs_rebuild("applications/docker/Dockerfile_proxyapps", "proxyapps",
                   dependencies=["swfft", "miniamr", "xsbench"], build_args=build_args)
file_needs_rebuild("applications/docker/Dockerfile_all", "all", dependencies=["demo", "proxyapps", "moose"],
                   build_args=build_args)
file_needs_rebuild("plugins/docker/Dockerfile_all", "plugins", dependencies=["performance"], build_args=build_args)

# Now, we wrap every package with the gui and the plugins.
for package in ["vnv", "performance", "plugins", "asgard", "heat", "simple", "miniamr", "swfft", "xsbench", "hypre",
                "petsc", "libmesh", "mfem", "moose", "all", "demo", "proxyapps"]:

    build_args = {
        "GUI_IMAGE": f"{REPO_OWNER}/gui:{TAG}",
        "PLUGIN_IMAGE": f"{REPO_OWNER}/plugins:{TAG}"
    }
    file_needs_rebuild("applications/docker/Dockerfile_wrap", f"{package}", tag=f"f{REFTAG}", otag=f"f{TAG}",
                       build_args=build_args, from_image=package, dependencies=["gui", "performance"])

    if PUSH_TO_GHCR:
        push_image(f"{REPO_OWNER}/{package}", tag=TAG)
        push_image(f"{REPO_OWNER}/{package}", tag=f"f{TAG}")

if PUSH_TO_GHCR:
    push_image(f"{REPO_OWNER}/env", tag=TAG)
    push_image(f"{REPO_OWNER}/gui", tag=TAG)

result = 0
print(REBUILD_INFO)
for key, value in REBUILD_INFO.items():
    if value[2] is False:
        result += 1

exit(result)
