package "g++"
package "zlib1g-dev"

require_recipe "misc::sudo_path"

path = node[:vagrant][:config][:vm][:shared_folders][:contrib][:guestpath]
version = node[:popc][:version]
config = node[:popc][:config]

execute "get-popc-source" do
  user "vagrant"
  command <<-EOH
  rm -rf /tmp/popc
  cp -R #{path}/#{version} /tmp/popc
  EOH
end


# Copy the node config file and install popc
cookbook_file "/tmp/popc-node-config" do
  source config
  owner "vagrant"
end


cookbook_file "/tmp/popc-node-paths" do
  source "paths"
  owner "vagrant"
end


execute "compile-popc" do
  user "vagrant"
  cwd "/tmp/popc"
  command <<-EOH
  ./configure
  make
  EOH
end


execute "install-popc" do
  cwd "/tmp/popc"
  command "make install </tmp/popc-node-config"
end


execute "update-popc-path" do
  command "cat /tmp/popc-node-paths >>/etc/profile"
  not_if "grep \"$(cat /tmp/popc-node-paths)\" /etc/profile"
end


execute "update-root-popc-path" do
  command "cat /tmp/popc-node-paths >>/root/.bashrc"
  not_if "grep \"$(cat /tmp/popc-node-paths)\" /root/.bashrc"
end


# This configuration step is needed because the `make install` command
# consumes the stdin before reaching the configuration step
execute "setup-popc" do
  command "/usr/local/popc/sbin/popc_setup </tmp/popc-node-config"
end


file "/tmp/popc-*" do
  action :delete
  backup false
end
