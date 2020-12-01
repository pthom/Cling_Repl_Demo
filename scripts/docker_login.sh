THIS_DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)
PARENT_DIR=$THIS_DIR/..
docker run --rm -it -p 8888:8888 -v $PARENT_DIR:/sources_docker cling_xeus /bin/bash
