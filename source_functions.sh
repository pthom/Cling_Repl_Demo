
function zz_docker_export_notebooks_preview() {
    ./scripts/tooling/docker_export_notebooks_preview.sh
}

function zz_docker_export_notebooks_preview_deploy() {
    zz_docker_export_notebooks_preview && \
    cp html_output/external/type_name/notebooks/typename/typename.md external/type_name/README.md
}
