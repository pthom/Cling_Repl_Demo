DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)
docker run --rm -it -v $DIR/../..:/sources_docker cling_xeus /srv/conda/bin/python /sources_docker/scripts/tooling/export_notebooks_preview.py
