
# Docker container in order to test cling

## Create the container image
````bash
./docker_create_image.sh # will build a docker image with cling (be patient)
````

## Use the container

````bash
./docker_login.sh
 # you are now inside the docker container, in the /sources_docker folder
 # /sources_docker is linked to FunctionalPlus/repl_cling on your host machine
````

Inside the container, run jupyter-notebook with the correct options.

````bash
jnote.sh
````
