#!/bin/bash
# Add this to the docker command bellow to start a shell in the image. (useful for debugging)
IMG=solvers

if [ $# == 0 ]
then
  docker run -it --entrypoint bash \
     --mount type=bind,source="$PWD",readonly,target="/home/solvers" \
     $IMG
else
  EXE=$1
  shift
  docker run \
    --mount type=bind,source="$PWD",readonly,target="/home/solvers" \
    --entrypoint $EXE $IMG $*
fi
