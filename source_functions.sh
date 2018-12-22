export BZZ_MAINDIR=$(pwd)
export ZCB_SERVER=ubuntu@code-ballads.net
export ZCB_GENERATED_ROOT=/MAIN/generated-notebooks

function zz_source() {
    cd $BZZ_MAINDIR
    source source_functions.sh
    cd -
}

function zz_docker_export_notebooks_preview() {
    ./scripts/tooling/docker_export_notebooks_preview.sh
}

function zz_docker_login() {
    docker run --rm -it -v $BZZ_MAINDIR:/sources_docker cling_xeus /bin/zsh
}

function zz_docker_login_notebook() {
    docker run --rm -it -v $BZZ_MAINDIR:/sources_docker -p 8888:8888 cling_xeus /bin/zsh
}


function zz_ct_git_push() {
    cd external/cleantype
    git push
    cd -
    git push
}

function zz_ct_commit_manual() {
    if [ "$#" -ne 1 ]; then
        echo "Need a commit message"
        return
    fi
    commit_msg=$1

    cd external/cleantype
    git add README.md notebooks/cleantype/cleantype.ipynb
    git commit -m "$commit_msg (docs)"
    cd -
    git add external/cleantype
    git commit -m "update submodule external/ $commit_msg"
}

function zz_ct_manual_update_and_push() {
    if [ "$#" -ne 1 ]; then
        echo "Need a commit message"
        return
    fi
    commit_msg=$1

    zz_docker_export_notebooks_preview
    cp html_output/external/cleantype/notebooks/cleantype/cleantype.md external/cleantype/README.md

    zz_ct_commit_manual $commit_msg
    zz_ct_git_push
}

function zz_html_output_server() {
    cd $BZZ_MAINDIR
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
    scp repl_cling.tgz $ZCB_SERVER:$ZCB_GENERATED_ROOT/cpp &&\
    cd -
    ssh $ZCB_SERVER "
        cd $ZCB_GENERATED_ROOT/cpp
        rm -rf repl_cling
        tar xvfz repl_cling.tgz
    "
}
