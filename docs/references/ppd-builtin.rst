.. _ppd-builtin:

Built-in parser types
=====================

The base parser implementation comes with a rich collection of both scalar and
composite built-in types and classes to decode standard POP messages not
involving newly defined classes.


Scalars
-------

The set of provided scalars include:

.. c:type:: string

   A simple ``parocstring`` XDR compatible decoder.

.. c:type:: uint
.. c:type:: int
.. c:type:: float

.. c:type:: popbool

   POP specific boolean decoder.
   
   The POP-C++ implementation doesn't encode booleans as defined by the XDR RFC.
   This alternate implementation provides a workaround.

.. c:type:: bool

   The XDR compliant equivalent of the ``popbool`` primitive.


Compound types
--------------

The set of provided complex and compound types include:

.. c:type:: accesspoint

   .. c:member:: string endpoint
   
.. c:type:: NodeInfo

   .. c:member:: string nodeId
   .. c:member:: string operatingSystem
   .. c:member:: float power
   .. c:member:: int cpuSpeed
   .. c:member:: float memorySize
   .. c:member:: int networkBandwidth
   .. c:member:: int diskSpace
   .. c:member:: string protocol
   .. c:member:: string encoding

.. c:member:: ExplorationListNode[] ExplorationList

.. c:type:: ExplorationListNode
   
   .. c:member:: string nodeId
   .. c:member:: array(string) visited

.. c:type:: ObjectDescription

   .. c:member:: float power0
   .. c:member:: float power1
   .. c:member:: float memory0
   .. c:member:: float memory1
   .. c:member:: float bandwidth0
   .. c:member:: float bandwidth1
   .. c:member:: float walltime
   .. c:member:: int manual
   .. c:member:: string cwd
   .. c:member:: int search0
   .. c:member:: int search1
   .. c:member:: int search2
   .. c:member:: string url
   .. c:member:: string user
   .. c:member:: string core
   .. c:member:: string arch
   .. c:member:: string batch
   .. c:member:: string joburl
   .. c:member:: string executable
   .. c:member:: string platforms
   .. c:member:: string protocol
   .. c:member:: string encoding
   .. c:member:: dict(string, string) attributes

.. c:type:: Request

   .. c:member:: string uid
   .. c:member:: int maxHops
   .. c:member:: optional(string) nodeId
   .. c:member:: optional(string) operatingSystem
   .. c:member:: optional(int) minCpuSpeed
   .. c:member:: optional(int) hasExpectedCpuSpeedSet
   .. c:member:: optional(float) minMemorySize
   .. c:member:: optional(float) expectedMemorySize
   .. c:member:: optional(int) minNetworkBandwidth
   .. c:member:: optional(int) expectedNetworkBandwidth
   .. c:member:: optional(int) minDiskSpace
   .. c:member:: optional(int) expectedDiskSpace
   .. c:member:: optional(float) minPower
   .. c:member:: optional(float) expectedPower
   .. c:member:: optional(string) protocol
   .. c:member:: optional(string) encoding
   .. c:member:: ExplorationList explorationList

.. c:type:: Response

   .. c:member:: string uid
   .. c:member:: NodeInfo nodeInfo
   .. c:member:: ExplorationList explorationList


.. c:type:: POPCSearchNode

   .. c:member:: float nodeid01
   .. c:member:: float nodeid02
   .. c:member:: float nodeid03
   .. c:member:: float nodeid04
   .. c:member:: float nodeid05
   .. c:member:: float nodeid06
   .. c:member:: float nodeid07
   .. c:member:: int nodeid08
   .. c:member:: string nodeid09
   .. c:member:: float nodeid10
   .. c:member:: float nodeid11
   .. c:member:: uint nodeid12
   .. c:member:: int nodeid13
   .. c:member:: int nodeid14
   .. c:member:: int nodeid15
   .. c:member:: int nodeid16
   .. c:member:: int nodeid17
   .. c:member:: int nodeid18
   .. c:member:: int nodeid19
   .. c:member:: int nodeid20
   .. c:member:: int nodeid21
   .. c:member:: int nodeid22
   .. c:member:: int nodeid23
   .. c:member:: string nodeid24
   .. c:member:: int nodeid25

   .. todo::
      Define the semantics of the members

.. c:type:: POPCSearchNodeInfo

   .. c:member:: string nodeId
   .. c:member:: string operatingSystem
   .. c:member:: float power
   .. c:member:: int cpuSpeed
   .. c:member:: float memorySize
   .. c:member:: int networkBandwidth
   .. c:member:: int diskSpace
   .. c:member:: string protocol
   .. c:member:: string encoding

Classes
~~~~~~~

The set of provided classes include:

.. py:class:: paroc_service_base

   .. py:method:: BindStatus() -> int, string, string
   .. py:method:: AddRef() -> int
   .. py:method:: DecRef() -> int
   .. py:method:: Encoding(string) -> bool
   .. py:method:: Kill() -> void
   .. py:method:: ObjectAlive() -> bool
   .. py:method:: ObjectAlive() -> void
   .. py:method:: Stop(string) -> bool

.. py:class:: CodeMgr

   .. py:method:: RegisterCode(string, string, string) -> void
   .. py:method:: QueryCode(string, string) -> string, int
   .. py:method:: GetPlatform(string) -> string, int

.. py:class:: RemoteLog

   .. py:method:: Log(string) -> void

.. py:class:: ObjectMonitor

   .. py:method:: ManageObject(string) -> void
   .. py:method:: UnManageObject(string) -> void
   .. py:method:: CheckObjects() -> int

.. py:class:: JobCoreService

   .. py:method:: CreateObject(string, string, ObjectDescription, int) -> int, string, int

.. py:class:: JobMgr

   .. py:method:: JobMgr(bool, string, string, string, string) -> void
   .. py:method:: RegisterNode(string) -> void
   .. py:method:: Reserve(ObjectDescription, int) -> float, int
   .. py:method:: ExecObj(string, ObjectDescription, int, int, int, string) -> int, string, int
   .. py:method:: GetNodeAccessPoint() -> string

.. py:class:: AppCoreService

   .. py:method:: AppCoreService(string, bool, string) -> void

.. py:class:: POPCSearchNode

   .. py:method:: POPCSearchNode(string, bool) -> void
   .. py:method:: setJobMgrAccessPoint(string) -> void
   .. py:method:: getJobMgrAccessPoint() -> string
   .. py:method:: setPOPCSearchNodeId(string) -> void
   .. py:method:: getPOPCSearchNodeId() -> string
   .. py:method:: setOperatingSystem(string) -> void
   .. py:method:: getOperatingSystem() -> string
   .. py:method:: setPower(float) -> void
   .. py:method:: getPower() -> float
   .. py:method:: setMemorySize(float) -> void
   .. py:method:: getMemorySize() -> int
   .. py:method:: setNetworkBandwidth(int) -> void
   .. py:method:: getNetworkBandwidth() -> int
   .. py:method:: addNeighbor(POPCSearchNode) -> POPCSearchNode
   .. py:method:: launchDiscovery(Request, int) -> array of POPCSearchNodeInfo
   .. py:method:: askResourcesDiscovery(Request, string, string) -> void
   .. py:method:: callbackResult(Response) -> void

.. py:class:: ParentProcess

   .. py:method:: callback() -> int, string

.. note::
   For the provided classes not all methods are defined yet. The provided
   definitions suffices for most basic measures involving other external 
   types, but it can be that some requests for more specific measures could not
   be decoded without extending the method definitions.
