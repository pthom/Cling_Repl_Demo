DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
# docker run --rm -it -v $DIR/..:/sources_docker cling_xeus /bin/zsh

docker run --rm -it -p 5900:5900 -v $DIR/..:/sources_docker cling_xeus /bin/zsh
