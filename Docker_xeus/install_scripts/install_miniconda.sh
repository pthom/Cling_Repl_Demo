
# install miniconde
mkdir -/install_scripts
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  -o $install_scripts/miniconda-install.sh
chmod +x $install_scripts/miniconda-install.sh
$install_scripts/miniconda-install.sh -b

echo "export PATH=$PATH:/root/miniconda3/bin" >> /root/.zshrc
echo "export PATH=$PATH:/root/miniconda3/bin" >> /root/.bashrc
