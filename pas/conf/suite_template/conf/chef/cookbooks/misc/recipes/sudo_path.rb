
execute "configure-sudo-path" do
  command "echo \"alias sudo='sudo env PATH=\\$PATH'\" >>/etc/profile"
  not_if "grep \"alias sudo='sudo env PATH=\\$PATH'\" /etc/profile"
end
