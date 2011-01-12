# Install from remote location

remote_file "popc" do
  path "/tmp/popc.tar.gz"
  source "http://gridgroup.hefr.ch/popc_1.3.1beta.tgz"
end

bash "untar-popc" do
  code "(rm -rf /tmp/popctmp ; rm -rf /tmp/popc ; mkdir -p /tmp/popctmp)"
  code "(tar -zxvf /tmp/popc.tar.gz -C /tmp/popctmp)"
  code "(mv /tmp/popctmp/* /tmp/popc ; rm -rf /tmp/popctmp)"
end
