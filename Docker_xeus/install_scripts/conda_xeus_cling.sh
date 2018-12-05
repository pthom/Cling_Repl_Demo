# install jupyter & xeus.cling
export PATH=$PATH:/root/miniconda3/bin

conda install jupyter
conda install -c QuantStack -c conda-forge xeus-cling

# jnote.sh = alias to run jupyter notebook with correct settings
echo "jupyter-notebook --allow-root --no-browser --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password='' " \
      >> /usr/local/bin/jnote.sh
chmod +x /usr/local/bin/jnote.sh
