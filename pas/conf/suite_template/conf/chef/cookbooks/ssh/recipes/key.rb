
execute "generate-key" do
  command "(yes y | ssh-keygen -qf /home/vagrant/.ssh/id_rsa -N \"\" -C $(getip eth1))"
  creates "/home/vagrant/.ssh/id_rsa"
  user "vagrant"
end
