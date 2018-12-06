DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
docker run --rm -it -v $DIR/..:/sources_docker cling_xeus /bin/zsh
