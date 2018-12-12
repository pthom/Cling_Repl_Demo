export ZZ_MAINDIR=$(pwd)
export ZZ_HTMLOUTPUT=$ZZ_MAINDIR/html_output
export CB_SERVER=ubuntu@code-ballads.net
export CB_GENERATED_ROOT=/MAIN/generated-notebooks

function zz_source() {
    cd $ZZ_MAINDIR
    source source_functions.sh
    cd -
}

function zz_docker_export_notebooks_preview() {
    ./scripts/tooling/docker_export_notebooks_preview.sh
}

function zz_docker_login() {
    docker run --rm -it -v $ZZ_MAINDIR:/sources_docker cling_xeus /bin/zsh
}

function zz_docker_login_notebook() {
    docker run --rm -it -v $ZZ_MAINDIR:/sources_docker -p 8888:8888 cling_xeus /bin/zsh
}


function zz_tn_git_push() {
    cd external/type_name
    git push
    cd -
    git push
}

function zz_tn_commit_manual() {
    if [ "$#" -ne 1 ]; then
        echo "Need a commit message"
        return
    fi
    commit_msg=$1

    cd external/type_name
    git add README.md notebooks/typename/typename.ipynb
    git commit -m "$commit_msg (docs)"
    cd -
    git add external/type_name
    git commit -m "update submodule external/ $commit_msg"
}

function zz_tn_manual_update_and_push() {
    if [ "$#" -ne 1 ]; then
        echo "Need a commit message"
        return
    fi
    commit_msg=$1

    zz_docker_export_notebooks_preview
    cp html_output/external/type_name/notebooks/typename/typename.md external/type_name/README.md

    zz_tn_commit_manual $commit_msg
    zz_tn_git_push
}

function zz_html_output_server() {
    cd $ZZ_MAINDIR
    python3 -m http.server
}

function zz_docker_run_notebook() {
    ./scripts/docker_run_notebook.sh
}


function zz_cb_deploy() {
    rm -rf /tmp/repl_cling &&\
    cp -a html_output /tmp/repl_cling &&\
    cd /tmp &&\
    tar cvfz repl_cling.tgz repl_cling &&\
    scp repl_cling.tgz $CB_SERVER:$CB_GENERATED_ROOT/cpp &&\
    cd -
    ssh $CB_SERVER "
        cd $CB_GENERATED_ROOT/cpp
        tar xvfz repl_cling.tgz
    "
}
