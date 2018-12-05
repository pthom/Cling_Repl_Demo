FROM ubuntu:18.04
WORKDIR /sources_docker
RUN apt-get update
RUN apt-get install -y build-essential python3 python3-pip zsh curl wget cmake ninja-build git


# install zsh & oh-my-zsh (so that we have nice colors)
RUN apt-get install -y zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true


RUN echo "export LC_ALL=C.UTF-8" >> /root/.zshrc
RUN echo "export LANG=C.UTF-8" >> /root/.zshrc
RUN echo "export PATH=/usr/local/bin:$PATH" >> /root/.zshrc


# install miniconde
RUN mkdir /root/install
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  -o /root/install/miniconda-install.sh
RUN chmod +x /root/install/miniconda-install.sh &&  /root/install/miniconda-install.sh -b
RUN echo "export PATH=$PATH:/root/miniconda3/bin" >> /root/.zshrc && \
          export PATH=$PATH:/root/miniconda3/bin
# install jupyter & xeus.cling
RUN export PATH=$PATH:/root/miniconda3/bin &&\
           conda install jupyter
RUN export PATH=$PATH:/root/miniconda3/bin &&\
           conda install -c QuantStack -c conda-forge xeus-cling

# install opencv via conda
RUN export PATH=$PATH:/root/miniconda3/bin &&\
    conda install opencv

# jnote = alias to run jupyter notebook
RUN echo "jupyter-notebook \
          --allow-root --no-browser --ip 0.0.0.0 \
           --NotebookApp.token='' --NotebookApp.password=''" \
           >> /usr/local/bin/jnote.sh && \
          chmod +x /usr/local/bin/jnote.sh


# # install virtual x11 server
# ADD install_scripts/install_x11vnc.sh /install_scripts/install_x11vnc.sh
# RUN /install_scripts/install_x11vnc.sh
# RUN apt-get install -y libgtk2.0-dev
# RUN echo "export DISPLAY=:0" >> /root/.zshrc





# # install gcc-7
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
# RUN apt-get update
# RUN apt-get install -y gcc-7 g++-7
# RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 80 && \
#     update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 80


# # update cmake
# RUN cd / && \
#     wget --no-verbose https://github.com/Kitware/CMake/releases/download/v3.13.1/cmake-3.13.1-Linux-x86_64.tar.gz && \
#     tar xvf cmake-3.13.1-Linux-x86_64.tar.gz && \
#     echo "export PATH=/cmake-3.13.1-Linux-x86_64/bin:$PATH" >> /root/.zshrc

# RUN echo "export LC_ALL=C.UTF-8" >> /root/.zshrc && \
#     echo "export LANG=C.UTF-8" >> /root/.zshrc && \
#     echo "alias python=python3" >> /root/.zshrc


# # download cling & add to the PATH
# RUN cd / && \
#     curl https://root.cern.ch/download/cling/cling_2018-12-03_ubuntu16.tar.bz2 -o cling.tgz
# RUN cd / && tar xvf cling.tgz
# RUN echo "export PATH=$PATH:/cling_2018-12-03_ubuntu16/bin" >> /root/.zshrc

# # get opencv source
# RUN cd / && git clone https://github.com/opencv/opencv.git
# # build opencv
# RUN cd /opencv && \
#     mkdir build && \
#     cd build && \
#     cmake -DCMAKE_BUILD_TYPE=RELEASE -GNinja .. \
#     -DBUILD_JAVA=OFF \
#     -DBUILD_PROTOBUF=OFF \
#     -DBUILD_PERF_TESTS=OFF \
#     -DBUILD_TEST=OFF \
#     -DBUILD_opencv_apps=OFF \
#     -DBUILD_opencv_java_bindings_generator=OFF \
#     -DBUILD_opencv_python_bindings_generator=OFF \
#     -DBUILD_opencv_gapi=OFF\
#     -DWITH_GTK=ON

# RUN cd /opencv/build && ninja && ninja install

# # install jupyter with C++ support
# RUN ln -s /cling_2018-12-03_ubuntu16 /cling
# RUN cd /cling/share/cling/Jupyter/kernel && \
#     pip3 install jupyter && \
#     pip3 install -e .
# RUN cd /cling/share/cling/Jupyter/kernel &&\
#     jupyter-kernelspec install  cling-cpp17 &&\
#     jupyter-kernelspec install  cling-cpp1z &&\
#     jupyter-kernelspec install  cling-cpp14 &&\
#     jupyter-kernelspec install  cling-cpp11

# # jupyter-notebook --allow-root --no-browser --ip 0.0.0.0
# RUN echo "jupyter-notebook --allow-root --no-browser --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''" >> /usr/local/bin/j-note.sh && chmod +x /usr/local/bin/j-note.sh

# RUN echo "export PATH=/cling/bin:$PATH" >> /root/.zshrc
