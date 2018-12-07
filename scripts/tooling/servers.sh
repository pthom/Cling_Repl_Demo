DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)
MAINDIR=$DIR/../..
$MAINDIR/scripts/html_output_server.sh &
$MAINDIR/scripts/docker_run_notebook.sh &
