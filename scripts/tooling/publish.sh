DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

MAINDIR=$DIR/../..
SERVER=212.83.137.58
USER=pascal
DST_DIR=HTML/

cd $MAINDIR
$DIR/docker_export_notebooks_preview.sh
cp -a html_output cpp_repl
tar cvfz cpp_repl.tgz cpp_repl
rm -rf cpp_repl
scp cpp_repl.tgz $USER@$SERVER:$DST_DIR

ssh $USER@$SERVER "
cd $DST_DIR
tar xvfz cpp_repl.tgz
rm cpp_repl.tgz
"
