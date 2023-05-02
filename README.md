# The VnV Toolkit Project:

Welcome to VnVLabs.com, where the cloud meets simplicity! With VnVLabs, you can easily provision on-demand resources on AWS using your own AWS account. And that's just the beginning.

Our platform boasts a simple and intuitive interface for provisioning and managing resources, including support for any EC2 instance type. Once you've provisioned a compute resource, simply ask VnVLabs to launch a docker container on that resource, and we'll take it from there.

We'll take your docker container and wrap it up inside our custom docker image, which includes an integrated VSCode-like IDE, an integrated Paraview Visualizer, and an integrated file browser. You can then interact with the IDE, Visualizer, and file browser through our web-based interface. It's that easy!

But we don't stop there. VnVLabs supports any Ubuntu-based docker image, so you can bring your own custom image and get started right away. And for developers who want even more control, we offer the VnVToolkit, a C/C++ API that can be used within C/C++ and FORTRAN applications. With the VnVToolkit, you can control how your software is presented within the VnVLabs GUI and take advantage of a range of verification and validation processes.

Our features include a built-in unit testing framework, function-level integration testing (configurable at runtime by the end-user), application-level integration testing, provenance tracking, input file validation, live data visualization using real simulation data, performance monitoring, uncertainty quantification, and sensitivity analysis.

So why wait? Try VnVLabs today and experience the power of cloud computing with the simplicity you deserve.
## Try it out:

### A Simple Demo Application.

The following docker command will launch a VnV container running on localhost pre installed with 
a range of VnV Applications. . You can navigate to localhost:5001 in the browser to see the GUI. 

    docker run --rm -it -p 5001:5001 ghcr.io/vnvlabs/all /vnv-gui/run.sh

Notes:
   1. The GUI runs inside a docker container where you (the user) has root access. You are logged in as root!
   2. All the source code for the various applications are in /source/* . Software with an install step was in installed in /software/*
   3. Your container will cease to exist as soon as you exit the docker run command. This is just for demo purposes. 

### Software As A Service
   
The following command will deploy the VnV Toolkits SAAS container wrapper. This wrapper lets users create and use containers 
prebuilt using VnV software. It is a really basic html front-end and flask based reverse proxy that allows users to manage the spinning 
up and shutting down of containers. 

    docker run --rm -it --network="host" -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/vnvlabs/serve

Notes:
   1. The default username is Admin. The password will be printed to standard out during initialization. 
   2. The container uses a docker-in-docker scheme to launch containers on behalf of the users. 
   3. When you exit the container, all user information will be lost --- BUT -- Any containers created by the container while it was alive will still be active. All containers launched by this application are given the prefix "vnv-"
   4. The container also allows users to snapshot a container. The images that result from this snapshot will exist beyond the end of the container. You will need to delete those manually. They also all have the prefix "vnv-"
   5. A universal volume is created for each user. This volume is mounted in the /data/ directory of every container launched by the user. This lets users transfer data between containers instantly. 
   6. All the containers run on the same machine -- the machine that is hosting the webserver. In the future, the SAAS deployment will support docker swarm and/or kubernetes to run containers using remote resources.
   7. Each User is given an account balance of $100 when they create an account. THIS BALANCE IS FAKE. It is just there as a mechanism for demostrating the containers abilitiy to track the uptime of each users containers. 

# Integrate VnV Into your code base

The process of integrating VnV into your codebase depends on the build system you are using. 

  ## CMAKE 
   
  The Core VnV library uses a CMAKE build system. As part of that install, it creates the appropriate 
  cmake files such that the library can be picked up using the standard CMAKE find_package function. Some examples include:
  
   - https://github.com/vnvlabs/heat
   - https://github.com/vnvlabs/simple
   - https://github.com/vnvlabs/asgard
   - https://github.com/vnvlabs/hypre
   - https://github.com/vnvlabs/mfem

  ## Other:
  
  It is a little bit harder to get VnV integrated into an autotools project, primarily because of the
  code generation step. However, it can be done. Some examples include:
  
  - https://github.com/vnvlabs/libmesh (Autotools project)
  - https://github.com/vnvlabs/petsc (Custom build system)
  - https://github.com/vnvlabs/xsbench (GNU Make)
 
# Project Layout:

Whereever possible, we have broken the codebase into single priority repositories. The main repos are:

   - vnvlabs A single cactch all repo containing submodule links to the various other repositories.
   - vnv : The core vnv API and runtime. 
   - gui : The flask implementation of the VnV Graphical user interface
   - server: A simple flask based reverse proxy and html front end for SAAS style deployment
   
# vnv-snippets: A Related VS Code Extension:

We created an extension for VS Code that enables users employ snippets for incorporating VnV macros.

## vnv-snippets' Repo:

https://marketplace.visualstudio.com/items?itemName=jburz2001.vnv-snippets

## vnv-snippets' VS Code Marketplace Page:
https://marketplace.visualstudio.com/items?itemName=jburz2001.vnv-snippets

# License:

Each repository contains its own licensing information. FFor the most part, all vnvlabs code (the core api,
the gui, the SAAS server and a few of the application examples) are released using the three clause BSD license. 

This repository includes a number of forks for third party software. All software forks (moose,libmesh,petsc,hypre,mfem,asgard,
swfft,xs-bench,miniamr,etc.) are simply exist only for demonstration and testing purposes. We will attempt to keep these forks up
to date with the upstream repositories, however, we make no claims that they are up to date at any given time. The hope is that our VnV 
modifications will eventually make their way into the upstream codebases, removing the need for the vnvlabs forks. 
   
   
   
   
