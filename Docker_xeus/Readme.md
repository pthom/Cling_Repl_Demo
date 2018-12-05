
# Docker container in order to test cling

## Create the container image
````bash
cd repl_cling/Docker/ubuntu
./docker_create_image.sh # will build a docker image with cling (be patient)
````

## Use the container

````bash
./docker_login.sh
 # you are now inside the docker container, in the /sources_docker folder
 # /sources_docker is linked to FunctionalPlus/repl_cling on your host machine
````

Inside the container, run a X server

````bash
/start_x_vnc_quiet.sh # run a X11 server
````

Launch a vnc viewer on your host machine and connect to `localhost` -> you will see the
screen of the docker container


Then, run the interactive sessions instructions given inside [../Readme.md](../Readme.md):


````cpp
cling --std=c++14

.L init.cpp
cv::Mat lena = cv::imread("lena.jpg");
cv::imshow("lena", lena); cv::waitKey(100);
//etc...
````
