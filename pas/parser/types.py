import __builtin__
from pas.parser import registry, errors
import xdrlib
from collections import namedtuple
from lxml import etree



class cls(object):
    def __init__(self, id, name, methods):
        self.id = id
        self.name = name
        self.methods = dict([(m.id, m) for m in methods])
        registry.current_registry.register_class(self)

    def __str__(self):
        return self.name

    def getmethod(self, methodid):
        try:
            return self.methods[methodid]
        except KeyError:
            raise errors.UnknownMethod(self, methodid)


class exc(cls):
    def __init__(self, id, name, properties):
        self.id = id
        self.name = name
        self.properties = properties
        registry.current_registry.register_exception(self)
    
    def arguments(self, decoder):
        return [p(decoder) for p in self.properties]

class func(object):
    def __init__(self, id, name, args, retypes):
        self.id = id
        self.name = name
        self.retypes = retypes
        self.args = args

    def toxml(self):
        el = etree.Element('method')
        attrs = el.attrib
        attrs['id'] = str(self.id)
        attrs['name'] = self.name
        
        return el

    def __str__(self):
        return self.name

    def arguments(self, decoder):
        return [a(decoder) for a in self.args]

    def result(self, decoder):
        return [r(decoder) for r in self.retypes]


def compound(name, *parts):
    model = namedtuple(name, ' '.join(p[0] for p in parts))

    def decoder(stream):
        return model(**dict([(name, type(stream)) for name, type in parts]))

    return decoder


def string(stream):
    return stream.unpack_string()[:-1]


def uint(stream):
    return xdrlib.Unpacker.unpack_uint(stream)


def int(stream):
    return xdrlib.Unpacker.unpack_int(stream)


def popbool(stream):
    """
    The POP-C++ implementation doesn't encode booleans as defined by the RFC.
    This alternate implementation provides a workaround.
    """
    return __builtin__.bool(stream.unpack_int() & 0xff000000)


def bool(stream):
    return xdrlib.Unpacker.unpack_bool(stream)


def float(stream):
    return xdrlib.Unpacker.unpack_float(stream)


def dict(key, value):
    def decoder(stream):
        return dict([(key(stream), value(stream)) for i in range(int(stream))])
    return decoder


def array(type):
    """
    Length prefixed array of homogeneous items.
    """
    # Work around to the standard xdrlib to provide the argument to the type
    # function as it is not passed by the unpack_farray method of the Unpacker
    # class. @see xdrlib.py:224
    # @todo: Discuss on py-dev about a possible improvement.
    def unpack(stream):
        def unpacker():
            return type(stream)
        return stream.unpack_array(unpack_item=unpacker)
    return unpack


def optional(type, unpack_bool=popbool):
    def unpack(stream):
        if unpack_bool(stream):
            return type(stream)
        else:
            return None
    return unpack


accesspoint = compound('AccessPoint',
    ('endpoint', string)
)

NodeInfo = compound('NodeInfo',
    ('nodeId', string),
    ('operatingSystem', string),
    ('power', float),
    ('cpuSpeed', int),
    ('memorySize', float),
    ('networkBandwidth', int),
    ('diskSpace', int),
    ('protocol', string),
    ('encoding', string),
)


ExplorationList = array(
    compound('ListNode',
        ('nodeId', string),
        ('visited', array(string)),
    )
)


ObjectDescription = compound('ObjectDescription',
    ('power0', float),
    ('power1', float),
    ('memory0', float),
    ('memory1', float),
    ('bandwidth0', float),
    ('bandwidth1', float),
    ('walltime', float),
    ('manual', int),
    ('cwd', string),
    ('search0', int),
    ('search1', int),
    ('search2', int),
    ('url', string),
    ('user', string),
    ('core', string),
    ('arch', string),
    ('batch', string),
    ('joburl', string),
    ('executable', string),
    ('platforms', string),
    ('protocol', string),
    ('encoding', string),
    ('attributes', dict(string, string)),
)


Request = compound('Request',
    ('uid', string),
    ('maxHops', int),
    ('nodeId', optional(string)),
    ('operatingSystem', optional(string)),
    ('minCpuSpeed', optional(int)),
    ('hasExpectedCpuSpeedSet', optional(int)),
    ('minMemorySize', optional(float)),
    ('expectedMemorySize', optional(float)),
    ('minNetworkBandwidth', optional(int)),
    ('expectedNetworkBandwidth', optional(int)),
    ('minDiskSpace', optional(int)),
    ('expectedDiskSpace', optional(int)),
    ('minPower', optional(float)),
    ('expectedPower', optional(float)),
    ('protocol', optional(string)),
    ('encoding', optional(string)),
    ('explorationList', ExplorationList)
)


Response = compound('Response',
    ('uid', string),
    ('nodeInfo', NodeInfo),
    ('explorationList', ExplorationList),
)


POPCSearchNode = compound('POPCSearchNode_UnknownSerializationFormat',
    ('nodeid01', float),
    ('nodeid02', float),
    ('nodeid03', float),
    ('nodeid04', float),
    ('nodeid05', float),
    ('nodeid06', float),
    ('nodeid07', float),
    ('nodeid08', int),
    ('nodeid09', string),
    ('nodeid10', float),
    ('nodeid11', float),
    ('nodeid12', uint),
    ('nodeid13', int),
    ('nodeid14', int),
    ('nodeid15', int),
    ('nodeid16', int),
    ('nodeid17', int),
    ('nodeid18', int),
    ('nodeid19', int),
    ('nodeid20', int),
    ('nodeid21', int),
    ('nodeid22', int),
    ('nodeid23', int),
    ('nodeid24', string),
    ('nodeid25', int),
)


POPCSearchNodeInfo = compound('POPCSearchNodeInfo',
    ('nodeId', string),
    ('operatingSystem', string),
    ('power', float),
    ('cpuSpeed', int),
    ('memorySize', float),
    ('networkBandwidth', int),
    ('diskSpace', int),
    ('protocol', string),
    ('encoding', string),
)














