# The VnVLabs Project:

VnVLabs is an simple, low-code framework for automated GUI building in scientific applications and libraries. The project consists of two parts:

   - vnv : The VnV Toolkit API is an interface between scientific software. 
   - gui : The VnV Graphical user interface 

## The VnV Graphical User Interface

[![Nightly Build and Release](https://github.com/vnvlabs/vnvlabs/actions/workflows/build.yml/badge.svg)](https://github.com/vnvlabs/vnvlabs/actions/workflows/build.yml)

The VnV Graphical User interface is a web-based user interface for designing, running and analyzing numerical simulations. The interface provides a built
in IDE (using Eclipe Theia), built in 3D visualization (using Paraview Visualizer), and a custom built application execution interface. The GUI can be hosted
locally, and on the web, making it an extremely effective approach for both local and remote development. 

That said, the true power of the VnV Graphical User Interface comes from its integration with the VnV Toolkit. The VnV Toolkit provides a large set of macros that, when 
included in your code base, allow for features like; auto completion of input files, runtime integration testing, performance monitoring, automatic report generation, live
data visualization and more. 

TODO: Add a gif

## A Simple Demo Application.

The easiest way to spin up a VnV GUI is with docker: 

    docker run --rm -it -p 5001:5001 ghcr.io/vnvlabs/all /vnv-gui/run.sh

Once that command is finished, navigate to localhost:5001 in the browser to see the GUI. This docker image includes a number of popular scientific 
applications that have been augmented with VnV Toolkit Macros to improve their functionality within the GUI. The application source is available 
int the /user/dev/source directory. It is installed in the "/user/dev/software" directory. 


## Integrate VnV Into your code base

The process of integrating VnV into your codebase depends on the build system you are using. 

## CMAKE 
VnV Ship the relavent CMakeFiles required to locate VnV on a machine using the cmake find_package function. Once found, users can use the 
link_vnv_file function to link there library. Here is a really simple example CMake File for a one file application. 
  
    cmake_minimum_required(VERSION 3.6)
    project(Heat)
    
    find_package(Injection REQUIRED)
    add_executable(heat "heat.cpp")
    link_vnv_file(heat Heat cpp)
  
We have integrated VnV into a number of different applications: 
   - https://github.com/vnvlabs/heat
   - https://github.com/vnvlabs/simple
   - https://github.com/vnvlabs/asgard
   - https://github.com/vnvlabs/hypre
   - https://github.com/vnvlabs/mfem

## Other:
 
The process of integrating the tool using non CMake Build Systems varies from application to application. The primary requirement is that you 
generate a compile_command.json file as part of the build. Some applications will already include targets to generate this file (i.e., MOOSE), and 
for other applications you will need to use a tool like "bear (TODO:Cite)" to generate the file. Once you have the file, you need to manually call 
the VnV code generation tool to generate the code required to integrate VnV (the CMake Integration does this automatically as part of the build). 

Some examples include:
  
  - https://github.com/vnvlabs/libmesh (Autotools project)
  - https://github.com/vnvlabs/petsc (Custom build system)
  - https://github.com/vnvlabs/xsbench (GNU Make)
 
# Project Layout:

The main repos are:
   - env: A dockerfile that installs all the dependencies required to get the toolkit, the plugins and the gui working on your machine. Use this as the base image when building a VnV docker image for your application.
   - vnv: The VnV Toolkit API. This needs to be installed if you want to use the VnV Toolkit customize the integration within the GUI.
   - plugins: A set of VnV Plugins that can be installed in addition to the toolkit to provide more VnV features (i.e., performance monitoring, UQ).

   - gui: This is the VnV GUI. The GUI is a Python Flask application. 
   - applications/: The directory contains a number of different scientific applications that we have added VnV toolkit macros too. 
    

# License:

Each repository contains its own licensing information. FFor the most part, all vnvlabs code (the core api,
the gui, the SAAS server and a few of the application examples) are released using the three clause BSD license. 

This repository includes a number of forks for third party software. All software forks (moose,libmesh,petsc,hypre,mfem,asgard, swfft,xs-bench,miniamr,etc.) are simply exist only for demonstration and testing purposes. We will attempt to keep these forks up to date with the upstream repositories, however, we make no claims that they are up to date at any given time. The hope is that our VnV modifications will eventually make their way into the upstream codebases, removing the need for the vnvlabs forks. 
   
   
   
   
