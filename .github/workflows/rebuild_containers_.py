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
parser.add_argument('--repo_owner', type=str, help='The owner of the container registry', default='ghcr.io/vnvlabs')
parser.add_argument('--tag', type=str, help='The version or branch of code to use', default='nightly')
parser.add_argument('--ref_tag', type=str, help='The reference tag', default='nightly')
parser.add_argument('--full_rebuild', action='store_true', help='Whether to perform a full rebuild')
parser.add_argument('--actually_build', action='store_false', help='Whether to actually build the image')
parser.add_argument('--cache_from_nightly', action='store_false', help='Whether to use nightly cache to build')
parser.add_argument('--push', action='store_true', help='Push at end')
parser.add_argument('--stage', type=str, help='Stage', default="env")
parser.add_argument('--gen', action='store_false', help='Gen workflow file')

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
STAGE= args.stage
BUILDING=args.gen

REBUILD_INFO = {}
docker_client = docker.from_env()




build_args = {"VERSION": TAG, "REPO": REPO_OWNER}

def ACTION(stage):
    return [
        {
            "name" : "checkout" , 
            "uses" : "actions/checkout@v3" 
        }, {
            "name" : "python" , 
            "uses" : "actions/setup-python@v2", 
            "with" : {
                "python-version" : "3.9"
            }
        }, {
            "name" : "docker" ,
            "uses" : "docker/login-action@v1", 
            "with" : {
                "registry" : "ghcr.io",
                "username" : "${{github.actor}}",
                "password" : "${{secrets.GITHUB_TOKEN}}"
            }
        }, {
            "name" : "Install Deps",
            "run" : "python -m pip install --upgrade pip && pip install docker"
        }, {
            "name" : "SSH TO HTTP",
            "run" : "python .github/workflows/ssh_to_https.py"
        }, {
            "name" : "Build Stage " + stage,
            "run" : "python .github/workflows/rebuild_containers_.py --push --stage " + stage 
        }
    ]


def JOB_WF(stage, header):
    header[stage] = {
        "runs-on" : "ubuntu-latest",
        "needs" : [ a.split(":")[0] for a in STAGES[stage].get("dependencies",[]) ],
        "steps" : ACTION(stage)
    }
    from_image = STAGES[stage].get("from_image")
    if from_image is not None:
        header[stage]["needs"].append(from_image)

def HEADER_WF():
   Y = {}
   Y["name"] = "Nightly Build and Release"

   Y["jobs"] = {}
   Y["on"] = {
       "schedule" : [{"cron" : '0 2 * * *'}],
       "workflow_dispatch" : {}
   }
   return Y


def DUMP_WORKFLOW_FILE():
     header = HEADER_WF()
     for stage in STAGES:
         JOB_WF(stage,header["jobs"])
     print(yaml.dump(header))     
    
    

STAGES = {
    "env" : dict(path="env/Dockerfile", reponame="env"),
    "gui" : dict(path="gui", reponame="gui", from_image=None),
    "vnv" : dict(path="vnv", reponame="vnv", from_image="env", from_tag=TAG),
    "performance" : dict(path="plugins/performance", reponame="performance", from_image="vnv", from_tag=TAG),
    "asgard" : dict(path="applications/asgard", reponame="asgard", from_image="vnv", from_tag=TAG),
    "heat" : dict(path="applications/asgard", reponame="asgard", from_image="vnv", from_tag=TAG),
    "simple" : dict(path="applications/simple", reponame="simple", from_image="vnv", from_tag=TAG),
    "miniamr" : dict(path="applications/miniamr", reponame="miniamr", from_image="vnv", from_tag=TAG),
    "swfft" : dict(path="applications/swfft", reponame="swfft", from_image="vnv", from_tag=TAG),
    "xsbench" : dict(path="applications/xsbench", reponame="xsbench", from_image="vnv", from_tag=TAG),
    "hypre" : dict(path="applications/hypre", reponame="hypre", from_image="vnv", from_tag=TAG),
    "petsc" : dict(path="applications/petsc", reponame="petsc", from_image="hypre", from_tag=TAG),
    "libmesh" : dict(path="applications/libmesh", reponame="libmesh", from_image="petsc", from_tag=TAG),
    "mfem" : dict(path="applications/mfem", reponame="mfem", from_image="petsc", from_tag=TAG),
    "moose" : dict(path="applications/moose", reponame="moose", from_image="libmesh", from_tag=TAG),
    "plugins" : dict(path="plugins/docker/Dockerfile_all", reponame="plugins", dependencies=[f"performance:{TAG}"], build_args=build_args),
    "demo" : dict(path="applications/docker/Dockerfile_demo", reponame="demo", dependencies=[f"simple:{TAG}", f"heat:{TAG}"], build_args=build_args),
    "proxyapps" : dict(path="applications/docker/Dockerfile_proxyapps", reponame="proxyapps", dependencies=[f"swfft:{TAG}", f"miniamr:{TAG}", f"xsbench:{TAG}"], build_args=build_args),
    "all" : dict(path="applications/docker/Dockerfile_all", reponame="all", dependencies=[f"asgard:{TAG}",f"simple:{TAG}", f"heat:{TAG}",f"swfft:{TAG}", f"miniamr:{TAG}", f"xsbench:{TAG}", f"moose:{TAG}"], build_args=build_args)
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
                              cachetag = f"f{REFTAG}"
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

def check_image_sha(image, tag=TAG, sha="none"):
    try:

        res = subprocess.check_output(['skopeo', 'inspect', f"docker://{image}:{tag}"]).decode('ascii')
        labs = json.loads(res)["Labels"]["vnvsha"]
        
        if labs != sha:
            return False, "SHA do not match"
        return True, "Dont rebuild"
    
    except Exception as e:
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

def needs_rebuild(path, reponame, cachetag=REFTAG, otag=TAG, repo=REPO_OWNER, from_image=None, from_tag=TAG, dependencies=[], **kwargs):
    
    if f"{reponame}:{otag}" in REBUILD_INFO:
        return
    
    REBUILD = True
    if os.path.isdir(path):
       REBUILD_SHA_TEMP = get_git_submodule_hash(path)
       REBUILD_SHA = REBUILD_SHA_TEMP[1:41]
       SUBMODULE_PULL = (REBUILD_SHA_TEMP[0] == "-")
    else:
       REBUILD_SHA = sha256sum(path)
       SUBMODULE_PULL = False
    
    if FULLREBUILD is False:
  
        if from_image is not None and f"{from_image}:{from_tag}" not in REBUILD_INFO:
            needs_rebuild(**(STAGES[ f"{from_image}"]))

        for image in dependencies:
            if image not in REBUILD_INFO:
                needs_rebuild(**STAGES[image.split(":")[0]])

        if from_image is None or REBUILD_INFO[f"{from_image}:{from_tag}"][0] is False:
            if True not in [REBUILD_INFO[a][0] for a in dependencies]:  # And none of the other deps were modified
                matches,reason = check_image_sha(repo_name(reponame, repo=repo), tag=cachetag, sha=REBUILD_SHA)
                if matches:
                    REBUILD = False
                else:
                    print("Rebuilding ", reponame  ," because ", reason)
            else:
                print("Rebuilding because one of the dependencies is rebuilt:",
                    [a for a in REBUILD_INFO.keys() if REBUILD_INFO[a][0]])
        else:
            print("Rebuilding because ", from_image, " was rebuilt")
    else:
        print("Rebuilding because full_rebuild was requested")
    
    REBUILD_INFO[f"{reponame}:{otag}"] = [REBUILD, REBUILD_SHA, SUBMODULE_PULL]

def actually_rebuild(path, reponame, repo=REPO_OWNER, otag=TAG, cachetag=REFTAG, from_image=None, from_tag=TAG, build_args={}, dependencies=[], dockerfile="docker/Dockerfile", **kwargs):

    if ACTUALLY_BUILD:

        if REBUILD_INFO[f"{reponame}:{otag}"][0]:

            if from_image is not None and REBUILD_INFO[f"{from_image}:{from_tag}"][0] is True:
                if not actually_rebuild(**(STAGES[f"{from_image}:{from_tag}"])):
                    print("Rebuild of from_image failed")
                    return False

            for i in dependencies:
                if REBUILD_INFO[i][0] is True:
                    if not actually_rebuild(**(STAGES[i.split(":")[0]])):
                        print("Skipping build because dependency ", i, " rebuild failed")
                        return False    

            print("Building: ", f"{repo_name(reponame, repo=repo)}:{otag}")

            if from_image is not None:
                pull_image(repo_name(from_image, repo=repo), tag=from_tag)
                build_args["FROM_IMAGE"] = f"{repo_name(from_image, repo=repo)}:{from_tag}"

            for image in dependencies:
                pull_image(repo_name(image.split(":")[0], repo=repo), tag=image.split(":")[1])

            if REBUILD_INFO[f"{reponame}:{otag}"][2]:
                init_and_update_submodule(path)

            isdir = os.path.isdir(path)

            if build_image(
                build_context=os.path.dirname(path) if not isdir else path ,
                dockerfile_rel_bc=os.path.basename(path) if not isdir else dockerfile,
                build_args=build_args,
                cache_from=[] if not CACHE_FROM_NIGHTLY else [f"{repo_name(reponame, repo=repo)}:{cachetag}"],
                repo_and_tag=f"{repo_name(reponame, repo=repo)}:{otag}",
                labels={"vnvsha": REBUILD_INFO[f"{reponame}:{otag}"][1] }
            ) is False:
                return False
            
            if PUSH_TO_GHCR:
                push_image(f"{repo_name(reponame, repo=repo)}", tag=otag)

        elif otag != cachetag:
            pull_image(repo_name(from_image, repo=repo), tag=cachetag)
            print("Skipping Build and Tagging: ", f"{repo_name(reponame, repo=repo)}:{otag}")
            rname1 = f"{repo_name(reponame, repo=repo)}:{cachetag}"
            docker_client.api.tag(image=rname1, repository=repo_name(reponame, repo=repo), tag=otag)
            if PUSH_TO_GHCR:
               push_image(f"{repo_name(reponame, repo=repo)}", tag=otag)

        else:
            print(f"{repo_name(reponame, repo=repo)}:{otag}", "does not need to be rebuilt")
        
        return True
    
    else:
        return True




if BUILDING:
    
   needs_rebuild(**(STAGES[STAGE]))
   res = actually_rebuild(**(STAGES[STAGE]))

   print(json.dumps(REBUILD_INFO, indent=3))
   exit(0 if res else 1)

else:
    DUMP_WORKFLOW_FILE()




