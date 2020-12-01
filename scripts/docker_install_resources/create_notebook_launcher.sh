# jnote = alias to run jupyter notebook with correct settings
echo "
#\!/bin/bash
jupyter notebook --allow-root --no-browser --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
" >> /usr/local/bin/jnote

chmod +x /usr/local/bin/jnote
