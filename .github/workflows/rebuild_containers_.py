import json

import docker
import hashlib
import subprocess
import os
import argparse
import yaml


# Create the argument parser
parser = argparse.ArgumentParser(description='Description of your script')

# Add the arguments
parser.add_argument('--repo_owner', type=str,
                    help='The owner of the container registry', default='ghcr.io/vnvlabs')
parser.add_argument(
    '--tag', type=str, help='The version or branch of code to use', default='nightly')
parser.add_argument('--ref_tag', type=str,
                    help='The reference tag', default='nightly')
parser.add_argument('--full_rebuild', action='store_true',
                    help='Whether to perform a full rebuild')
parser.add_argument('--actually_build', action='store_false',
                    help='Whether to actually build the image')
parser.add_argument('--cache_from_nightly', action='store_false',
                    help='Whether to use nightly cache to build')
parser.add_argument('--push', action='store_true', help='Push at end')
parser.add_argument('--stage', type=str, help='Stage', default="env")
parser.add_argument('--gen', type=int, help='0 for build, 1 for release, 2 for local, 3 to generate github workflow')
parser.add_argument('--verbose', action='store_true', help='Verbose')
parser.add_argument('--release', type=str, help="release version", default="")
parser.add_argument('--local', action='store_true', help='Run locally in serial')

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
STAGE = args.stage
BUILDING = args.gen
VERBOSE = args.verbose
RUN_LOCAL = False
REBUILD_INFO = {}
docker_client = docker.from_env()


build_args = {"VERSION": TAG, "REPO": REPO_OWNER}


def ACTION(stage, extra=[]):
    a = [
        {
            "name": "checkout",
            "uses": "actions/checkout@v3"
        }, {
            "name": "python",
            "uses": "actions/setup-python@v2",
            "with": {
                "python-version": "3.9"
            }
        }, {
            "name": "docker",
            "uses": "docker/login-action@v1",
            "with": {
                "registry": "ghcr.io",
                "username": "${{github.actor}}",
                "password": "${{secrets.GITHUB_TOKEN}}"
            }
        }, {
            "name": "Install Deps",
            "run": "python -m pip install --upgrade pip && pip install docker pyyaml"
        }, {
            "name": "SSH TO HTTP",
            "run": "python .github/workflows/ssh_to_https.py"
        }]

    b = [{
        "name": "Build Stage " + stage,
        "run": "python .github/workflows/rebuild_containers_.py --push --stage " + stage
    }]

    return a + extra + b


def JOB_WF(stage, header):
    header[stage] = {
        "runs-on": "ubuntu-latest",
        "needs": [a.split(":")[0] for a in STAGES[stage].get("dependencies", [])],
        "steps": ACTION(stage, extra=STAGES[stage].get("extra", []))
    }
    from_image = STAGES[stage].get("from_image")
    if from_image is not None:
        header[stage]["needs"].append(from_image)


def HEADER_WF():
    Y = {}
    Y["name"] = "Nightly Build and Release"
    Y["on"] = {
        "schedule": [{"cron": '0 2 * * *'}],
        "workflow_dispatch": {}
    }
    Y["jobs"] = {}
    return Y


def DUMP_WORKFLOW_FILE():

    header = HEADER_WF()
    for stage in STAGES:
        JOB_WF(stage, header["jobs"])
    print("#This file is autogenerated by calling rebuild_containers_.py with the command --gen. Go edit that file instead.")
    print(yaml.dump(header, sort_keys=False))


gui_extra = [
    {
        "name": "download-paraview",
        "uses": "actions/cache@v3",
        "id": "download-paraview",
        "with": {
              "path": "./pv.tar.gz",
              "key": "download-paraview"
        }
    }, {
        "if": "${{steps.download-paraview.outputs.cache-hit != 'true'}}",
        "name": "Download the binary",
        "run": "git submodule update --init gui && cd gui && ./download_paraview.sh"
    }
]

STAGES = {
    "env": dict(path="env/Dockerfile", reponame="env"),
    "gui": dict(path="gui", reponame="gui", from_image=None, extra=gui_extra),
    "vnv": dict(path="vnv", reponame="vnv", from_image="env", from_tag=TAG),
    "performance": dict(path="plugins/performance", reponame="performance", from_image="vnv", from_tag=TAG),
    "asgard": dict(path="applications/asgard", reponame="asgard", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "heat": dict(path="applications/heat", reponame="heat", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "simple": dict(path="applications/simple", reponame="simple", from_image="vnv", from_tag=TAG,  dockerfile="vnv/Dockerfile"),
    "miniamr": dict(path="applications/miniamr", reponame="miniamr", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "swfft": dict(path="applications/swfft", reponame="swfft", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "xsbench": dict(path="applications/xsbench", reponame="xsbench", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "hypre": dict(path="applications/hypre", reponame="hypre", from_image="vnv", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "petsc": dict(path="applications/petsc", reponame="petsc", from_image="hypre", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "libmesh": dict(path="applications/libmesh", reponame="libmesh", from_image="petsc", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "mfem": dict(path="applications/mfem", reponame="mfem", from_image="petsc", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "moose": dict(path="applications/moose", reponame="moose", from_image="libmesh", from_tag=TAG, dockerfile="vnv/Dockerfile"),
    "plugins": dict(path="plugins/Dockerfile_all", reponame="plugins", dependencies=[f"performance:{TAG}"], build_args=build_args),
    "demo": dict(path="applications/docker/Dockerfile_demo", reponame="demo", dependencies=[f"simple:{TAG}", f"heat:{TAG}"], build_args=build_args),
    "proxyapps": dict(path="applications/docker/Dockerfile_proxyapps", reponame="proxyapps", dependencies=[f"swfft:{TAG}", f"miniamr:{TAG}", f"xsbench:{TAG}"], build_args=build_args),
    "all": dict(path="applications/docker/Dockerfile_all", reponame="all", dependencies=[f"asgard:{TAG}", f"simple:{TAG}", f"heat:{TAG}", f"swfft:{TAG}", f"miniamr:{TAG}", f"xsbench:{TAG}", f"moose:{TAG}"], build_args=build_args)
}



package_build_args = {
    "GUI_IMAGE": f"{REPO_OWNER}/gui:{TAG}",
    "PLUGIN_IMAGE": f"{REPO_OWNER}/plugins:{TAG}"
}

for package in ["vnv", "performance", "plugins", "asgard", "heat", "simple", "miniamr", "swfft", "xsbench", "hypre", "petsc", "libmesh", "mfem", "moose", "all", "demo", "proxyapps"]:
    STAGES[f"f{package}"] = dict(path="applications/docker/Dockerfile_wrap",
                                 reponame=f"{package}",
                                 otag=f"f{TAG}",
                                 from_image=package,
                                 from_tag=TAG,
                                 dependencies=[f"gui:{TAG}", f"plugins:{TAG}"],
                                 build_args=package_build_args,
                                 cachetag=f"f{REFTAG}"
                                 )


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

def get_image_labels(image, tag=TAG, lab="vnvsha"):
        res = subprocess.check_output(
            ['skopeo', 'inspect', f"docker://{image}:{tag}"]).decode('ascii')

        return json.loads(res)["Labels"]
    

def check_image_sha(image, tag=TAG, sha="none", lab="vnvsha"):
    try:

        res = subprocess.check_output(
            ['skopeo', 'inspect', f"docker://{image}:{tag}"]).decode('ascii')

        labes = json.loads(res)["Labels"]
        if lab not in labes:
            return False, f"Label {lab} Does not Exist"

        labs = labes[lab]
        if labs != sha:
            return False, "SHA do not match"
        return True, "Dont rebuild"

    except Exception as e:
        print(e)
        return False, "Exception getting label"


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
                if VERBOSE:
                    print(output["stream"].strip())
                else:    
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


def get_sha_from_path(path):
    if os.path.isdir(path):
        REBUILD_SHA_TEMP = get_git_submodule_hash(path)
        return REBUILD_SHA_TEMP[1:41]
    else:
        return sha256sum(path)



def needs_rebuild(path, reponame, cachetag=REFTAG, otag=TAG, repo=REPO_OWNER, from_image=None, from_tag=TAG, dependencies=[], **kwargs):

    if FULLREBUILD:
        print("Full rebuild requested")
        return True

    # If repo has changed since last rebuild,
    matches, reason = check_image_sha(repo_name(reponame, repo=repo), tag=cachetag, sha=get_sha_from_path(path), lab="vnvsha")
    if not matches:
        print("repo has changed")
        return True

    # If needs rebuild because from_image was rebuilt or a dependency was rebuilt.
 
    labels = get_image_labels(repo_name(reponame, repo=repo), tag=cachetag)

    all_deps = dependencies if from_image is None else dependencies + [f"{from_image}:{from_tag}"]    
    for image in all_deps:
        print("Checking dep ", image)
        image_split = image.split(":")
        label = f"vnv_dep_sha_{image.replace(':','_')}"
        last_build_sha = labels.get(label,"<dne>")
        dep_labels = get_image_labels(repo_name(image_split[0], repo=repo), tag=image_split[1])
        if dep_labels.get("vnvsha","<dlabel>") != last_build_sha:
            print("Dep label ",  dep_labels.get("vnvsha","<dlabel>"), " Does not equal last build sha ", last_build_sha)
            return True       
       
    return False


def rebuild_if_needs(path, reponame, repo=REPO_OWNER, otag=TAG, cachetag=REFTAG, from_image=None, from_tag=TAG, build_args={}, dependencies=[], dockerfile="docker/Dockerfile", **kwargs):

    if needs_rebuild(path, reponame, otag=otag, cachetag=cachetag, repo=repo, from_image=from_image, from_tag=from_tag, dependencies=dependencies):

        # Set up the cache.
        cachefrom = []
        if CACHE_FROM_NIGHTLY:
            # Pull the last nightly image so we can use its cache.
            pull_image(repo_name(reponame, repo=repo), tag=cachetag)
            cachefrom = [f"{repo_name(reponame, repo=repo)}:{cachetag}"]

        # Pull rthe latest version of from_image
        if from_image is not None:
            pull_image(repo_name(from_image, repo=repo), tag=from_tag)
            build_args["FROM_IMAGE"] = f"{repo_name(from_image, repo=repo)}:{from_tag}"

        # Pull all of the dependencies
        for image in dependencies:
            pull_image(repo_name(image.split(":")[
                       0], repo=repo), tag=image.split(":")[1])

        # Set all of the vnv labels needed to determine if rebuild needed.
        all_deps = dependencies if from_image is None else dependencies + [f"{from_image}:{from_tag}"]
        labs = { "vnvsha" :  get_sha_from_path(path) }
        for dep in all_deps:
            spl = dep.split(":")
            labs[ f"vnv_dep_sha_{dep.replace(':','_')}" ] = get_image_labels(repo_name(spl[0], repo=repo), tag=spl[1])["vnvsha"]
         
        
        isdir = os.path.isdir(path)

        if isdir:
            init_and_update_submodule(path)

        args = dict(
            build_context=os.path.dirname(path) if not isdir else path,
            dockerfile_rel_bc=os.path.basename(path) if not isdir else dockerfile,
            build_args=build_args,
            cache_from=cachefrom,
            repo_and_tag=f"{repo_name(reponame, repo=repo)}:{otag}",
            labels=labs
        )

        if not ACTUALLY_BUILD:
            print("Dry run:\n", json.dumps(args,indent=4))
        else:
            if not build_image(**args):
                return False

            if PUSH_TO_GHCR:
                push_image(f"{repo_name(reponame, repo=repo)}", tag=otag)

    elif otag != cachetag:
        # if no rebuild required but we are giving it a new tag.
        
        pull_image(repo_name(from_image, repo=repo), tag=cachetag)
        print("Skipping Build and Tagging: ",
              f"{repo_name(reponame, repo=repo)}:{otag}")
        rname1 = f"{repo_name(reponame, repo=repo)}:{cachetag}"
        if ACTUALLY_BUILD:
            docker_client.api.tag(image=rname1, repository=repo_name(
                reponame, repo=repo), tag=otag)
            if PUSH_TO_GHCR:
                push_image(f"{repo_name(reponame, repo=repo)}", tag=otag)

    else:
        print(f"{repo_name(reponame, repo=repo)}:{otag}",
              "does not need to be rebuilt")

    return True



def release(version, repo=REPO_OWNER, rtag=TAG):
    for KEY,VALUE in STAGES.items():
        pull_image(repo_name(KEY, repo=repo), tag=rtag)
        docker_client.api.tag(image=f"{repo_name(KEY, repo=repo)}:{rtag}", repository=repo_name(KEY,repo=repo), tag=version)
        push_image(repo_name(KEY,repo=repo), tag=version)





if BUILDING == 0 :
    exit(0 if rebuild_if_needs(**(STAGES[STAGE])) else 1)
elif BUILDING == 1 and len(RELEASE_VERSION):
    release(RELEASE_VERSION)
elif BUILDING == 2:
  done = set()
  while len(done) < len(STAGES.keys()):
    for key,value in STAGES.items():
        
        if key in done:
            continue
        elif "from_image" not in value or value["from_image"] is None or value["from_image"] in done:
            
            b = True
            for dep in value.get("dependencies",[]):
                if dep.split(":")[0] not in done:
                    b = False
                    break
            if b:
                done.add(key)
                print("Building ", key)
                #Build it cause all deps are done
                if not rebuild_if_needs(**value):
                    print("Build failed")
                    exit(1)
  
            
            
             
        
else:
    DUMP_WORKFLOW_FILE()
