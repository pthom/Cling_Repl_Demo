export ZZ_MAINDIR=$(pwd)
export ZZ_HTMLOUTPUT=$ZZ_MAINDIR/html_output
export ZZ_NGINX_ROOT=$ZZ_MAINDIR/root_nginx
export ZZ_NGINX_DOCKERNAME=code_ballads_nginx

function zz_docker_export_notebooks_preview() {
    ./scripts/tooling/docker_export_notebooks_preview.sh
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
    ./scripts/html_output_server.sh &
}

function zz_docker_run_notebook() {
    ./scripts/docker_run_notebook.sh
}

function zz_nginx_deploy_content() {
    echo "ZZ_NGINX_ROOT=$ZZ_NGINX_ROOT"
    mkdir -p $ZZ_NGINX_ROOT/cpp
    cp -a $ZZ_HTMLOUTPUT $ZZ_NGINX_ROOT/cpp/repl_cling
}

function zz_nginx_run_server() {
    docker run --name $ZZ_NGINX_DOCKERNAME -v $ZZ_NGINX_ROOT:/usr/share/nginx/html:ro  -p 80:80 -d nginx
}

function zz_nginx_stop_server() {
    docker stop $ZZ_NGINX_DOCKERNAME
}

function zz_nginx_rm_server() {
    docker stop $ZZ_NGINX_DOCKERNAME
    docker rm $ZZ_NGINX_DOCKERNAME
}
