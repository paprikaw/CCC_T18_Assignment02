cd ~
GO_FILE=go1.20.3.linux-amd64.tar.gz
sudo wget https://go.dev/dl/${GO_FILE}
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.20.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
rm ${GO_FILE}

git clone https://github.com/containernetworking/plugins
cd plugins
git checkout v1.1.1
./build_linux.sh
sudo mkdir -p /opt/cni/bin
sudo cp bin/* /opt/cni/bin/
cd ..
rm -rf plugins