export OS="xUbuntu_22.04"
export VERSION="1.24"
export PUBLIC_KEY_1="648ACFD622F3D138"
export PUBLIC_KEY_2="0E98404D386FA1D9"

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $PUBLIC_KEY_1 
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $PUBLIC_KEY_2 

echo 'deb http://deb.debian.org/debian buster-backports main' | sudo tee /etc/apt/sources.list.d/backports.list
sudo apt update
sudo apt install -y -t buster-backports libseccomp2 || sudo apt update -y -t buster-backports libseccomp2

echo "deb [signed-by=/usr/share/keyrings/libcontainers-archive-keyring.gpg] https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
echo "deb [signed-by=/usr/share/keyrings/libcontainers-crio-archive-keyring.gpg] https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list

mkdir -p /usr/share/keyrings
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/libcontainers-archive-keyring.gpg
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/libcontainers-crio-archive-keyring.gpg

sudo apt-get update
sudo apt-get install -y cri-o cri-o-runc