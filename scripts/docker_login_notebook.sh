DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
docker run --rm -it -v $DIR/..:/sources_docker -p 8888:8888 cling_xeus /bin/zsh
