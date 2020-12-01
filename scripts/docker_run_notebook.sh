DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)

echo "Please wait until the server is launched, and browse to: 

http://localhost:8888

"


docker run --rm -it -p 8888:8888 -v $DIR/..:/sources_docker cling_xeus /bin/bash  -c "cd /sources_docker/notebooks && /usr/local/bin/jnote"
# open http://localhost:8888
