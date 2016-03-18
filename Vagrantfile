$script = <<SCRIPT
sudo apt-get install -y software-properties-common
sudo apt-add-repository -y ppa:git-core/ppa
sudo apt-get -qq update
sudo apt-get install -y git python3 python3-dev python3-pip python3.4-venv software-properties-common python-pip python-dev
sudo pip install cookiecutter
SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

  config.vm.provision "shell", inline: $script

end
