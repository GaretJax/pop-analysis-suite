#from pas import commands, jobmgr, measure, case
#from pas.conf import settings
#from pas.case import select
#
#def getparser(parser):
#    commands.case_argument(parser)
#
#@commands.select_case
#def command(options):
#    
#    local, remote = settings.paths['test-cases']
#    local, name = options.case
#    
#    jobmgr.kill()
#    measure.kill()
#    
#    measure.start(name)
#    jobmgr.startall()
#    case.execute(name)
#    jobmgr.stopall()
#    measure.stop(name)
#    
#    
#    
#    
#    commands.report.command(options)
#
#

#pas jobmgr kill ; pas measure kill ; pas measure start simple ; pas jobmgr start ; pas execute simple ; pas jobmgr stop ; pas measure stop simple ; pas measure collect simple ; pas measure toxml simple ; pas measure simplify simple ; pas measure decode simple ; pas measure report simple