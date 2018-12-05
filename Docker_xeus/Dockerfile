FROM ubuntu:18.04

ARG install_scripts=/install_scripts
ADD install_scripts/install_base.sh $install_scripts/install_base.sh
RUN $install_scripts/install_base.sh

ADD install_scripts/install_miniconda.sh $install_scripts/install_miniconda.sh
RUN $install_scripts/install_miniconda.sh

ADD install_scripts/conda_xeus_cling.sh $install_scripts/conda_xeus_cling.sh
RUN $install_scripts/conda_xeus_cling.sh

ADD install_scripts/conda_opencv.sh $install_scripts/conda_opencv.sh
RUN $install_scripts/conda_opencv.sh

# symlink /srv/conda required for path compatibility with mybinder.org
RUN mkdir -p /src && ln -s /root/miniconda3 /srv/conda

WORKDIR /sources_docker
