Complex VM setups
=================

The standard configuration provides a master-salve virtual machine setup with
two virtual machines. It is clearly possible to add many more machines to a
test environment and the task is made very easy by the means provided by the
``vagrant`` tool.

The process of adding a new virtual machine to the system is a 3-step process:

 1. Configure the new virtual machine inside the ``Vagrantfile`` by following
    the `vagrant documentation <http://vagrantup.com/docs/multivm.html>`_ or
    simply by copying one of the existing configuration blocks inside the
    ``Vagrantfile``, like the one presented in the following code snippet:
    
    .. code-block:: ruby
      
       config.vm.define :slaveX do |slaveX_config|
          slaveX_config.vm.network "33.33.33.15"
          slaveX_config.vm.provision :chef_solo do |chef|
             chef.cookbooks_path = "conf/chef/cookbooks"
             chef.roles_path = "conf/chef/roles"
             chef.add_role "slave"
             chef.json.merge!({:popc => {:version => "popc_1.3.1beta_xdr",}})
          end
       end
    
    .. note::
       If you opt for the copy and past approach, remember to change the IP
       address and the name of the new virtual machine.
              

 2. Boot up and provision the newly created virtual machine. To do so, simply
    run::
    
       $ vagrant up

 3. Add the IP of the newly created virtual machine to the :data:`ROLES
    <pas.conf.basesettings.ROLES>` settings directive inside the environment
    specific settings file::
    
       ROLES = {
           'master': ['33.33.33.10'],
           'client': ['33.33.33.10'],
           'slaves': ['33.33.33.11', '33.33.33.15'],
       }