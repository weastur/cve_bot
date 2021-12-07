# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/impish64"

  config.vm.synced_folder ".", "/home/vagrant/cve_bot"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "cve_bot"
    vb.gui = false
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y htop python3 python3-dev python3-pip python3-setuptools python3-wheel python3.9-venv
    cd cve_bot
    python3 -m venv .venv
    source ./.venv/bin/activate
    pip install setuptools wheel
    pip install -e '.[dev]'
  SHELL
end
