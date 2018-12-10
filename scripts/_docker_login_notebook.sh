DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)
docker run --rm -it -v $DIR/..:/sources_docker -p 8888:8888 cling_xeus /bin/zsh
