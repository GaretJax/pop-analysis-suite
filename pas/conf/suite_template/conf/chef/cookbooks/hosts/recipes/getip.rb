cookbook_file "/usr/local/bin/getip" do
  source "getip.sh"
  mode 0755
  owner "root"
  group "root"
end
