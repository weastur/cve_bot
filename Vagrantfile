# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/fedora34"

  config.vm.synced_folder ".", "/home/vagrant/cve_bot"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "cve_bot"
    vb.gui = false
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo dnf install -y htop python3 python3-devel python3-pip python3-setuptools python3-wheel
    cd cve_bot
    python3 -m venv .venv
    source ./.venv/bin/activate
    pip install --disable-pip-version-check setuptools wheel
    pip install --disable-pip-version-check -e '.[dev]'
  SHELL
end
