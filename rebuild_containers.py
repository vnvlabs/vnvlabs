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
parser.add_argument('--actually_build', action='store_true', help='Whether to actually build the image')

# Parse the arguments
args = parser.parse_args()

# Access the values of the arguments
REPO_OWNER = args.repo_owner
TAG = args.tag
REFTAG = args.ref_tag
FULLREBUILD = args.full_rebuild
ACTUALLY_BUILD = args.actually_build

REBUILD_INFO = {}
docker_client = docker.from_env()
docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
def repo_name(name,repo=REPO_OWNER):
    return f"{repo}/{name}"

def get_git_revision_hash(directory):
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory).decode('ascii').strip()

#Get a hash for a file
def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
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


def build_image(build_context, dockerfile_rel_bc, repo_and_tag, build_args, labels):
    generator = docker_client.api.build(path=build_context,
                            dockerfile=dockerfile_rel_bc,
                            tag=repo_and_tag,
                            buildargs=build_args,
                            decode=True,
                            labels=labels)
    while True:
        try:
            output = generator.__next__()
            if 'stream' in output:
                print(output['stream'].strip())
            elif "error" in output:
                print(output["error"])
                exit(1)
        except StopIteration:
            print("Docker image build complete.")
            break
        except ValueError:
            print("Error parsing output from docker image build: %s" % output)


def file_needs_rebuild(path, reponame, tag=REFTAG, repo=REPO_OWNER, from_image=None, otag=TAG, build_args={}, dependencies=[]):
    #Step 1a Check if we need to build env
    REBUILD = True
    REBUILD_SHA = sha256sum(path)
    if FULLREBUILD is False:
       if from_image is None or REBUILD_INFO[from_image][0] is False:
         if True not in [REBUILD_INFO[a][0] for a in dependencies]:  # And none of the other deps were modified
           image = pull_image(repo_name(reponame,repo=repo), tag=tag)
           if image is not None and "vnvsha" in image.labels:
              if image.labels["vnvsha"] == REBUILD_SHA:
                REBUILD = False

    REBUILD_INFO[reponame] = [REBUILD,REBUILD_SHA]
    
    if ACTUALLY_BUILD and "demo" in REBUILD_INFO:
      if REBUILD:
        print("Building: ", f"{repo_name(reponame,repo=repo)}:{otag}")

        if from_image is not None:
            build_args["FROM_IMAGE"] = f"{repo_name(from_image,repo=repo)}:{otag}"

        build_image(
            build_context=os.path.dirname(path),
            dockerfile_rel_bc=os.path.basename(path),
            build_args = build_args,
            repo_and_tag=f"{repo_name(reponame,repo=repo)}:{otag}",
            labels={"vnvsha":REBUILD_SHA}
        )
      else:
        print("Skipping Build and Tagging: ", f"{repo_name(reponame,repo=repo)}:{otag}")
        rname= f"{repo_name(reponame, repo=repo)}:{tag}"
        docker_client.api.tag(image=rname, repository=repo_name(reponame,repo=repo), tag=otag)


def repo_needs_rebuild(path, reponame, tag=REFTAG, repo=REPO_OWNER, from_image=None, dockerfile="docker/Dockerfile", otag=TAG, build_args ={}, dependencies=[]):
    #Step 3: Check if we need to rebuild the gui
    REBUILD = True
    REBUILD_SHA = get_git_revision_hash(os.path.abspath(path))
    
    #Check to see if we can skip rebuild. Cant skip if any of deps are rebuilt. 
    try:
     if FULLREBUILD is False: #If we didnt request a full rebuild
       if from_image is None or REBUILD_INFO[from_image][0] is False: #and the from_image was not modified
          if True not in [ REBUILD_INFO[a][0] for a in dependencies ]: #And none of the other deps were modified
            nightly = pull_image(repo_name(reponame,repo=repo), tag=tag) 
            if nightly is not None and "vnvsha" in nightly.labels: #If the docker file has not been modified
              if nightly.labels["vnvsha"] == REBUILD_SHA:
                REBUILD=False #then we dont need to rebuild cause all of the deps have not changed. 
    except Exception as e:
        print("Building because error ",e)
        pass

    REBUILD_INFO[reponame] = [REBUILD,REBUILD_SHA]

    if ACTUALLY_BUILD and "demo" in REBUILD_INFO:
      if REBUILD:
        print("Building ", f"{repo_name(reponame,repo=repo)}:{otag}")
        if from_image is not None:
            build_args["FROM_IMAGE"] = f"{repo_name(from_image,repo=repo)}:{otag}"

        build_image(
            build_context=path,
            dockerfile_rel_bc=dockerfile,
            build_args = build_args,
            repo_and_tag=f"{repo_name(reponame,repo=repo)}:{otag}",
            labels={"vnvsha":REBUILD_SHA}
        )
      else:
        print("Skipping Build and Tagging: ", f"{repo_name(reponame,repo=repo)}:{otag}")
        rname = f"{repo_name(reponame, repo=repo)}:{tag}"
        docker_client.api.tag(image=rname, repository=repo_name(reponame, repo=repo), tag=otag)

#Step 1a Check if we need to build env
file_needs_rebuild("env/Dockerfile", "env")
repo_needs_rebuild("gui","gui", from_image=None)
repo_needs_rebuild("vnv","vnv", from_image="env")
repo_needs_rebuild("plugins/performance","performance", from_image="vnv")
repo_needs_rebuild("applications/asgard", "asgard", from_image="vnv")
repo_needs_rebuild("applications/heat", "heat", from_image="vnv")
repo_needs_rebuild("applications/simple", "simple", from_image="vnv")
repo_needs_rebuild("applications/miniamr", "miniamr", from_image="vnv")
repo_needs_rebuild("applications/swfft", "swfft", from_image="vnv")
repo_needs_rebuild("applications/xsbench", "xsbench", from_image="vnv")
repo_needs_rebuild("applications/hypre", "hypre", from_image="vnv")
repo_needs_rebuild("applications/petsc", "petsc", from_image="hypre")
repo_needs_rebuild("applications/libmesh", "libmesh", from_image = "petsc")
repo_needs_rebuild("applications/mfem", "mfem", from_image = "petsc")
repo_needs_rebuild("applications/moose", "moose", from_image = "libmesh")

#Look at some multistage builds:
build_args = {"VERSION" : TAG, "REPO" : REPO_OWNER}
file_needs_rebuild("applications/docker/Dockerfile_demo", "demo", dependencies=["simple","heat"], build_args=build_args)
file_needs_rebuild("applications/docker/Dockerfile_proxyapps", "proxyapps", dependencies=["swfft","miniamr","xsbench"], build_args=build_args)
file_needs_rebuild("applications/docker/Dockerfile_all", "all", dependencies=["demo","proxyapps","moose"], build_args=build_args)
file_needs_rebuild("plugins/docker/Dockerfile_all", "plugins", dependencies=["performance"], build_args=build_args)

#Now, we wrap every package with the gui and the plugins. 
for package in ["vnv", "plugins","asgard","heat","simple","miniamr","swfft","xsbench","hypre","petsc","libmesh","mfem","moose", "all","demo","proxyapps"]:

    build_args = {
        "GUI_IMAGE" : f"{REPO_OWNER}/gui:{TAG}",
        "PLUGIN_IMAGE" : f"{REPO_OWNER}/plugins:{TAG}"
    }
    file_needs_rebuild("applications/docker/Dockerfile_wrap", f"{package}_full", build_args=build_args,from_image=package, dependencies=["gui","performance"])




