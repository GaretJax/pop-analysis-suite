name "slave"

description "Set up the JobMgr for a master POPC node"

run_list(
  "recipe[popc]",
  "recipe[hosts::getip]",
  "recipe[wireshark::tshark]",
  "recipe[screen]",
  "recipe[ssh::key]"
)

default_attributes :popc => {:config => "slaves"}

