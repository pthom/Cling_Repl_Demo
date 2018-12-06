DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
open http://localhost:8888
docker run --rm -it -p 8888:8888 -v $DIR/..:/sources_docker cling_xeus /bin/bash  -c "cd /sources_docker/examples/notebooks && /usr/local/bin/jnote"
