DIR="$(dirname "$(greadlink -f "$0")")" # readlink on linux (brew install coreutils on mac)
cd $DIR/../html_output
open http://localhost:8000
python3 -m http.server
