
# Docker container in order to test cling

## Create the container image
````bash
./docker_create_image.sh # will build a docker image with cling (be patient, this requires 10 minutes)
````

## Use the container

### Run it

````bash
./docker_login.sh
 # you are now inside the docker container, in the /sources_docker folder
 # /sources_docker is linked to this repo sources on your host machine
````

### Use it

#### use cling in the console
````bash
cling --std=c++14
````

#### use cling inside notebook

Inside the container, run jupyter-notebook with the correct options:
````bash
jnote.sh
````

Then, open your browser at http://localhost:8888
