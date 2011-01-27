"""

"""


import xdrlib
from pas.parser import messages


class MappingProtocol(object):

    request_types = ('request', 'response', 'exception')

    def __init__(self, types_registry):
        self.types_registry = types_registry

    def read_header(self, stream):
        return [stream.unpack_uint() for i in range(4)]

    def decode_full_frame(self, stream):
        req_type, classid, methodid, semantics = self.read_header(stream)

        handler = getattr(self, 'handle_' + self.request_types[req_type])
        message = handler(classid, methodid, semantics, stream)

        try:
            stream.done()
        except xdrlib.Error as e:
            #print "*" * 80
            #print repr(message)
            #r = decoder.get_buffer()
            #rem = decoder.get_position()
            #print repr(r)
            #print " " * (len(repr(r[:rem]))-3),
            #print repr(r[rem:])
            #print str(rem) + "/" + str(length)
            #print "*" * 80
            e.stream = stream
            e.message = message
            raise

        return message

    def handle_request(self, classid, methodid, semantics, decoder):
        cls = self.types_registry.get_class(classid)
        mth = cls.getmethod(methodid)
        sem = messages.Semantics(semantics)

        args = mth.arguments(decoder)

        return messages.POPRequest(sem, cls, mth, args, decoder.get_buffer())

    def handle_response(self, classid, methodid, _, decoder):
        cls = self.types_registry.get_class(classid)
        mth = cls.getmethod(methodid)

        result = mth.result(decoder)

        return messages.POPResponse(cls, mth, result, decoder.get_buffer())

    def handle_exception(self, classid, _1, _2, decoder):
        exc = self.types_registry.get_exception(classid)

        properties = exc.properties(decoder)

        return messages.POPException(exc, properties, decoder)


