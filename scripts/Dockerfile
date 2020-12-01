FROM continuumio/miniconda3
RUN apt-get update

# symlink /srv/conda required for path compatibility with mybinder.org
RUN mkdir -p /srv && ln -s /opt/conda /srv/conda

# Create a conda environment named "notebook", with cling + jupyter
# (see scripts/docker_install_resources/environment.yml)
# The environment name should be "notebook" for compatibility with mybinder.org
ADD docker_install_resources/environment.yml /docker_install_resources/environment.yml
RUN conda env create -f /docker_install_resources/environment.yml -n notebook

ADD docker_install_resources/ /docker_install_resources
RUN /docker_install_resources/create_notebook_launcher.sh

# RUN conda init --system
RUN echo "conda activate notebook" >> ~/.bashrc

COPY docker_install_resources/conda_entry_point.sh /docker_install_resources/conda_entry_point.sh
ENTRYPOINT ["/docker_install_resources/conda_entry_point.sh"]

WORKDIR /sources_docker
