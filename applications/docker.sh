#!/bin/bash
set -e 
set -o pipefail

BASE_IMG=$1
REPO_OWNER=$2
REON=$3
MODIFIED=$4



check_and_build "asgard" ${BASE_IMG}
check_and_build "heat" ${BASE_IMG}
check_and_build "simple" ${BASE_IMG}
check_and_build "miniamr" ${BASE_IMG}
check_and_build "swfft" ${BASE_IMG}
check_and_build "hypre" ${BASE_IMG}
check_and_build "petsc" "hypre"
check_and_build "mfem" "petsc"
check_and_build "libmesh" "petsc"
check_and_build "moose" "libmesh"

