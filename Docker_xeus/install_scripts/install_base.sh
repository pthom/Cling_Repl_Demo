
apt-get update
apt-get install -y build-essential python3 python3-pip zsh curl wget cmake ninja-build git tree htop

# install zsh & oh-my-zsh (so that we have nice colors)
apt-get install -y zsh
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

echo "export LC_ALL=C.UTF-8" >> /root/.zshrc
echo "export LC_ALL=C.UTF-8" >> /root/.bashrc
echo "export LANG=C.UTF-8" >> /root/.zshrc
echo "export LANG=C.UTF-8" >> /root/.bashrc
echo "export PATH=/usr/local/bin:$PATH" >> /root/.zshrc
echo "export PATH=/usr/local/bin:$PATH" >> /root/.bashrc
