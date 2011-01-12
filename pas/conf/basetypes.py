from pas.parser.types import *


cls(0, 'paroc_service_base', [
    func(0, 'BindStatus', [], [int, string, string]),   # broker_receive.cc:183
    func(1, 'AddRef', [], [int]),                       # broker_receive.cc:218
    func(2, 'DecRef', [], [int]),                       # broker_receive.cc:238
    func(3, 'Encoding', [string], [bool]),              # broker_receive.cc:260
    func(4, 'Kill', [], []),                            # broker_receive.cc:287
    func(5, 'ObjectAlive', [], [bool]),                 # broker_receive.cc:302
    func(6, 'ObjectAlive', [], []),                     # broker_receive.cc:319
    func(14,'Stop', [string], [bool]),                  #
])

cls(2, 'CodeMgr', [
    func(13, 'RegisterCode', [string, string, string], []),
    func(14, 'QueryCode', [string, string], [string,int]),
    func(15, 'GetPlatform', [string], [string, int]),
])

cls(3, 'RemoteLog', [
    func(13, 'Log', [string], []),  # remotelog.cc:17
])

cls(4, 'ObjectMonitor', [
    func(14, 'ManageObject', [string], []),
    func(15, 'UnManageObject', [string], []),
    func(16, 'CheckObjects', [], [int]),
])

cls(10, 'JobCoreService', [
    func(12, 'CreateObject', [string, string, ObjectDescription, int], [int, string, int]),
])

cls(15, 'JobMgr', [                             # jobmgr.ph:152
    #func(11, 'JobMgr', [bool, string, string, string], []),
    func(12, 'JobMgr', [bool, string, string, string, string], []),
    func(14, 'RegisterNode', [string], []), # jobmgr.ph:164
    func(18, 'Reserve', [ObjectDescription, int], [float, int]),
    func(20, 'ExecObj', [string, ObjectDescription, int, int, int, string], [int, string, int]),
    func(24, 'GetNodeAccessPoint', [], [string]), # jobmgr.ph:196
])

cls(20, 'AppCoreService', [
    func(11, 'AppCoreService', [string, bool, string], [])
])

cls(1001, 'POPCSearchNode', [
    func(11, 'POPCSearchNode', [string, bool], []),                     # popc_search_node.ph:51
    func(13, 'setJobMgrAccessPoint', [string], []),
    func(14, 'getJobMgrAccessPoint', [], [string]),
    func(15, 'setPOPCSearchNodeId', [string], []),
    func(16, 'getPOPCSearchNodeId', [], [string]),
    func(17, 'setOperatingSystem', [string], []),
    func(19, 'setPower', [float], []),
    func(23, 'setMemorySize', [float], []),
    func(25, 'setNetworkBandwidth', [int], []),
    func(33, 'addNeighbor', [POPCSearchNode], [POPCSearchNode]), # Something is wrong here
    func(36, 'launchDiscovery', [Request, int], [array(POPCSearchNodeInfo)]),
    func(37, 'askResourcesDiscovery', [Request, string, string], []),
    func(38, 'callbackResult', [Response], []),
])

cls(1500, 'TestClass', [
    func(10, 'TestClass',               [],                                                 []),
    func(12, 'get',                     [],                                                 [int]),
])

cls(1114117, 'WhatTheFuck', [
    func(0, 'Constructor', [], [int, string]),
])

