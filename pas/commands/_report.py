#"""
#
#"""
#
#
#import os
#from datetime import datetime
#import glob
#from lxml import etree
#
#from pas import shell, commands, tshark
#from pas.conf import settings, role, map_interfaces
#from pas.case import select
#
#
#def getparser(parser):
#    commands.case_argument(parser)
#
#
#def save(name):
#    """
#    Moves the relevant files to the shared directory and cleans up the
#    workspace.
#    """
#    
#    ip = '$(getip eth1)'
#    
#    l = settings.paths['local-measures'][1]
#    s = settings.paths['shared-measures'][1]
#    d = os.path.join(s, name, ip)
#    
#    shell.remote('mkdir -p "{}"'.format(d))
#    shell.remote('mv {}/* "{}"'.format(l, d))
#    #shell.remote('rm -rf "{}"'.format(l), sudo=True)
#
#
#def simplify(name):
#    from pas import xml
#    
#    path = os.path.join(settings.paths['shared-measures'][0], name)
#    files = []
#    
#    tr = xml.Transformation('conf/templates/simplify.xsl')
#    
#    for p in os.listdir(path):
#        p = os.path.join(path, p)
#        
#        for source in glob.glob('{}/*.xml'.format(p)):
#            dest = source.replace('.xml', '.simple.xml')
#            tr.transform(source, dest)
#            xml.format(dest)
#    
#    
#    #source = os.path.join(measure, '33.33.33.10', 'simple.eth1.xml')
#    #dest = source.replace('.xml', '.simple.xml')
#
#    #
#    #format(dest, True)
#
#
#
#
#
#@commands.select_case
#def command(options):
#    d = settings.paths['local-measures'][1]
#    f = settings.display_filter
#    
#    local, remote = settings.paths['test-cases']
#    local, name = options.case
#    
#    final_name = "{}_{}".format(name, datetime.now().strftime('%Y-%m-%d_%H:%M'))
#    
#    for host, interfaces in map_interfaces():
#        with shell.workon(host):
#            # Change the ownership of the temporary measures folder to be able
#            # to work on it as a normal user
#            shell.remote('chown -R {0}:{0} {1}'.format(settings.vm_user, d), sudo=True)
#            
#            # Step 1: Convert all raw measure files to XML using tshark
#            for i in interfaces:
#                raw, xml = ['{}/{}.{}.{}'.format(d, name, i, ext) for ext in ('raw', 'xml')]
#                tshark.pcaptoxml(raw, xml, f)
#            
#            # Step 2: Collect the files from the various VMs in a central location
#            save(final_name)
#    
#    # 3. Simplify original XML files (xslt transform)
#    simplify(final_name)
#    
#    # 4. Decode simplified XML file
#    decode(final_name)
#    
#    # 5. Generate report
#    
#    