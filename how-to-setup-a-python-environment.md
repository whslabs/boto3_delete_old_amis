# How to setup a python environment

# Create a VM
```sh
(
name=python

curl -o preseed.cfg https://www.debian.org/releases/bullseye/example-preseed.txt
cat <<EOF >> preseed.cfg
d-i grub-installer/bootdev string default
d-i netcfg/get_hostname string debian11-$name
d-i passwd/root-login boolean false
d-i passwd/user-fullname string whs
d-i passwd/user-password password magic
d-i passwd/user-password-again password magic
d-i passwd/username string whs
d-i preseed/late_command string apt-install openssh-server
popularity-contest popularity-contest/participate boolean false
tasksel tasksel/first multiselect standard
EOF
virt-install \
  --disk size=${more_storage:-20} \
  --initrd-inject preseed.cfg \
  --location https://deb.debian.org/debian/dists/bullseye/main/installer-amd64/ \
  --memory ${more_memory:-2048} \
  --name debian11-$name \
  --network bridge:virbr0 \
  --os-variant debian11 \
  --vcpus ${more_cpu:-2} \
  ;
) &
```

# Install python build dependencies
https://github.com/pyenv/pyenv/wiki
```sh
sudo apt-get install -y \
  build-essential \
  curl \
  libbz2-dev \
  libffi-dev \
  liblzma-dev \
  libncursesw5-dev \
  libreadline-dev \
  libsqlite3-dev \
  libssl-dev \
  libxml2-dev \
  libxmlsec1-dev \
  llvm \
  make \
  tk-dev \
  wget \
  xz-utils \
  zlib1g-dev \
  ;
```

# Install pyenv
```sh
curl https://pyenv.run | bash
cat <<'EOF' >> ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
source ~/.bashrc
```

# Install python
```sh
pyenv update
pyenv install 3.10.5
pyenv global 3.10.5
```

# Create virtualenv
```sh
pyenv virtualenv env1
pyenv activate env1
```

# Install black
```sh
pip install black
```

# Install pip-tools
```sh
pip install pip-tools
```
