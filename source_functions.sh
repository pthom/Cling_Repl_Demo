
function zz_docker_export_notebooks_preview() {
    ./scripts/tooling/docker_export_notebooks_preview.sh
}

function zz_docker_export_notebooks_preview_deploy() {
    zz_docker_export_notebooks_preview && \
    cp html_output/external/type_name/notebooks/typename/typename.md external/type_name/README.md
}

function zz_commit_tn_manual() {
    # set -e
    # zz_docker_export_notebooks_preview_deploy && \
    cd external/type_name
    git add README.md notebooks/typename/typename.ipynb
    git commit -m "Update typename.ipynb & readme.md"
    cd -
    git add external/type_name
    git commit -m "update submodule external/typename (updated manual)"
}

function zz_html_output_server() {
    ./scripts/html_output_server.sh &
}

function zz_docker_run_notebook() {
    ./scripts/scripts/docker_run_notebook.sh.sh &
}