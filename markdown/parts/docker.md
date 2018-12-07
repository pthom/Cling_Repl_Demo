
# Docker container in order to run these demos

The Dockerfile provided here will install `cling`, `miniconda`, `jupyter`, `xeus cling` , `opencv`; and it will configure
jupyter notebook so that you can access it from your host computer.

## Create the container image

````bash
./scripts/docker_create_image.sh # will build a docker image with cling (be patient, this requires 10 minutes)
````

## Use the container

### Run a notebook server inside docker

````bash
./scripts/docker_run_notebook.sh
````

Then, open your browser to http://localhost:8888

### use cling in the console

#### First log into the container:
````bash
> ./scripts/docker_login.sh
[DOCKER] /sources_docker > # You are now inside the docker container !
````

#### Then, from inside the container, launch cling:

````bash
cling --std=c++14
````

Then inside cling, enter some C++ commands : you can follow the example given [here](../Shell_Functional_REPL.html).
