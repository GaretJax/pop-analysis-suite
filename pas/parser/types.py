import __builtin__
from pas.parser import registry, errors
import xdrlib
from collections import namedtuple
from lxml import etree

# pylint: disable-msg=C0103,C0111

class cls(object):
    """
    Allows to define and automatically register a new POP class.
    
    :param id: The classid to which this class will be mapped.
    :param name: The name to use as string representation of this class.
                 Normally its always the original class name.
    :param methods: The list of methods bound to an instance of this class.
    
    :type id: int
    :type name: ``str`` or ``unicode`` compatible object
    :type methods: list of :ref:`pas.parser.types.func` objects
    """
    def __init__(self, id, name, methods):
        self.id = id
        self.name = name
        self.methods = __builtin__.dict([(m.id, m) for m in methods])
        registry.current_registry.register_class(self)

    def __str__(self):
        return self.name

    def getmethod(self, methodid):
        try:
            return self.methods[methodid]
        except KeyError:
            raise errors.UnknownMethod(self, methodid)


class exc(cls):
    """
    Allows to define and automatically register a new POP exception type.
    
    :param id: The exception ID to which this exception will be mapped.
    :param name: The name to use as string representation of this exception.
                 Normally its always the original exception name.
    :param properties: The list of properties bound to an instance of this
                       exception.
    
    :type id: int
    :type name: ``str`` or ``unicode`` compatible object
    :type properties: list of POP Parser DSL types
    """
    def __init__(self, id, name, properties):
        self.id = id
        self.name = name
        self.properties = properties
        registry.current_registry.register_exception(self)
    
    def arguments(self, decoder):
        return [p(decoder) for p in self.properties]

class func(object):
    """
    Allows to define a new POP method bound to a specific class instance. The
    method itself will never know to which class it belongs; to bind a method
    to a class insert it in the ``methods`` argument at class declaration time.
    
    :param id: The method ID to which this method will be mapped.
    :param name: The name to use as string representation of this method.
                 Normally its always the original method name.
    :param args: A list of arguments taken by this method. The provided types
                 will be directly used to decode the payload. Any built-in or
                 custom defined scalar or complex type is accepted.
    :param retypes: A list of types of the values returned by this method. The
                    provided types will be directly used to decode the payload.
                    Any built-in or custom defined scalar or complex type is
                    accepted.
                    
                    Note that an ``[out]`` argument will be present in the
                    POP response and shall thus be inserted into the
                    ``retypes`` list.
    
    :type id: int
    :type name: ``str`` or ``unicode`` compatible object
    :type args: list of POP Parser DSL types
    :type retypes: list of POP Parser DSL types
    """
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


def string(stream):
    return stream.unpack_string()[:-1]


def uint(stream):
    return stream.unpack_uint()


def int(stream):
    return stream.unpack_int()


def popbool(stream):
    """
    The POP-C++ implementation doesn't encode booleans as defined by the RFC.
    This alternate implementation provides a workaround.
    """
    return __builtin__.bool(stream.unpack_int() & 0xff000000)


def bool(stream):
    return stream.unpack_bool()


def float(stream):
    return stream.unpack_float()



def compound(name, *parts):
    """
    Creates a new compound type consisting of different parts. The parts are
    specified by the ``parts`` argument and read one adter the other from the
    POP payload.
    
    :param name: The name to give to the new type, used when pretty printing
                 the value.
    :param parts: The actual definition of the compound type.
    :type parts: list of ``(name, type)`` tuples
    
    Use it like this::
        
        NewType = compound('NewTypeName',
            ('member_1', string),
            ('member_2', int),
            ('member_3', float)
            # ...
        )
        
    """
    model = namedtuple(name, ' '.join(p[0] for p in parts))

    def decoder(stream):
        return model(**__builtin__.dict([(name, type(stream)) for name, type in parts]))

    return decoder


def dict(key, value):
    """
    Creates a new complex type mapping keys to values. All keys will share the
    same value type and so will all values.
    
    :param key: The type to use to decode the key.
    :param value: The type to use to decode the value.
    
    Use it like this::
        
        # SomeCompoundType.dict_member will hold a mapping of strings to integers
        
        SomeCompoundType = compound('SomeCompountTypeName',
            # ...other members...
            ('dict_member', dict(string, float)),
        )
        
    """
    def decoder(stream):
        return __builtin__.dict([(key(stream), value(stream)) for i in range(int(stream))])
    return decoder


def array(type):
    """
    Creates a new complex type representing a length prefixed array of
    homogeneous items.
    
    :param type: The type of each item in the array.
    
    Use it like this::
    
        # SomeCompoundType.array_member will hold a variable length array of ints
    
        SomeCompoundType = compound('SomeCompountTypeName',
            # ...other members...
            ('array_member', array(int)),
        )
    
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
    """
    Special composer type which allows to declare a structure member as
    optional. An optional member is member prefixed by a ``bool`` flag; the
    flag is first read, if it yields ``true``, it means that the value was
    encoded and it can be read, if it yields ``false``, it means that no value
    was encoded and the member is skipped.
    
    :param type: The type of the optional value.
    :param unpack_bool: The type to use to decode the boolean flag. Defaults
                        to :c:type:`popbool`, but can be changed to ``bool`` if
                        the encoding is done in an RPC compliant way.
    :type unpack_bool: callable
    
    Use it like this::

       # SomeCompoundType.optional_member will hold a string if it was encoded
       # or None if it was not encoded

       SomeCompoundType = compound('SomeCompountTypeName',
           # ...other members...
           ('optional_member', string),
       )

    """
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
    ('encoding', string)
)


ExplorationList = array(
    compound('ListNode',
        ('nodeId', string),
        ('visited', array(string))
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
    ('attributes', dict(string, string))
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
    ('explorationList', ExplorationList)
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
    ('nodeid25', int)
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
    ('encoding', string)
)














