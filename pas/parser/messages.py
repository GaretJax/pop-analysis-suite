

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from lxml import etree
from cStringIO import StringIO


try:
    import pytidy
except ImportError:
    from pas import pytidy


class Semantics(object):
    def __init__(self, sem):
        self.semantics = sem

    def toxml(self):
        semantics = etree.Element('semantics')
        attrs = semantics.attrib
        attrs['sync'] = str(int(self.sync))
        attrs['async'] = str(int(self.async))
        attrs['seq'] = str(int(self.seq))
        attrs['conc'] = str(int(self.conc))
        attrs['mutex'] = str(int(self.mutex))
        attrs['construct'] = str(int(self.construct))
        
        return semantics

    def __str__(self):
        if self.conc:
            s = 'conc'
        elif self.mutex:
            s = 'mutex'
        else:
            s = 'seq'

        s += ' sync' if self.sync else ' async'

        if self.construct:
            s += ' construct'

        return s

    @property
    def construct(self):
        return bool(self.semantics & 4)

    @property
    def sync(self):
        return bool(self.semantics & 1)

    @property
    def async(self):
        return not self.sync

    @property
    def mutex(self):
        return bool(self.semantics & 16)

    @property
    def conc(self):
        return bool(self.semantics & 8)

    @property
    def seq(self):
        return not self.mutex and not self.conc


class POPRequest(object):
    
    type = 'request'
    
    def __init__(self, semantics, klass, method, arguments, buffer):
        self.semantics = semantics
        self.klass = klass
        self.method = method
        self.arguments = arguments
    
    def toxml(self):
        el = etree.Element('request')
        el.attrib['classid'] = str(self.klass.id)
        el.attrib['class'] = self.klass.name
        mth = self.method.toxml()
        
        for t, a in zip(self.method.args, self.arguments):
            arg = etree.SubElement(mth, 'arg')
            arg.attrib['type'] = t.__name__
            arg.text = repr(a)
        
        el.append(self.semantics.toxml())
        el.append(mth)
        
        etree.SubElement(el, 'repr').text = repr(self)
        etree.SubElement(el, 'short').text = str(self)
        
        etree.SubElement(el, 'highlighted').append(
            etree.fromstring(self.formatted())
        )
        
        return el

    def __str__(self):
        args = map(repr, self.arguments)
        
        s = "{self.klass}.{self.method!s}(".format(self=self)
        
        l = 100 - len(s)
        ar = []
        
        for a in args:
            if l - len(a) < 0:
                s += ', '.join(ar) + (', ' if ar else '') + '...)'
                break
            
            ar.append(a)
        else:
            s += ', '.join(ar) + ')'
        return s

    def formatted(self):
        complete = "{self.klass}.{self.method!s}({args})".format(**{
            'self': self,
            'args': ', '.join(map(repr, self.arguments)),
        })
        
        # Tidy up python code
        res = StringIO()
        pytidy.tidy_up(StringIO(complete), res)
        code = res.getvalue().split('\n', 2)[-1].strip()
        
        # Highlight code
        return highlight(
            code,
            PythonLexer(),
            HtmlFormatter(cssclass="codehilite", style="pastie")
        )
        

    def __repr__(self):
        return "--> {self.klass}.{self.method!s}({args})".format(**{
            'self': self,
            'args': ', '.join(map(repr, self.arguments)),
        })


class POPResponse(object):
    
    type = 'response'
    
    def __init__(self, klass, method, result, buffer):
        self.klass = klass
        self.method = method
        self.result = result

    def formatted(self):
        complete = "{self.klass}.{self.method!s}({args})".format(**{
            'self': self,
            'args': ', '.join(map(repr, self.result)),
        })

        # Tidy up python code
        res = StringIO()
        pytidy.tidy_up(StringIO(complete), res)
        code = res.getvalue().split('\n', 2)[-1].strip()

        # Highlight code
        return highlight(
            code,
            PythonLexer(),
            HtmlFormatter(cssclass="codehilite", style="pastie")
        )

    def toxml(self):
        el = etree.Element('response')
        el.attrib['classid'] = str(self.klass.id)
        el.attrib['class'] = self.klass.name
        mth = self.method.toxml()
        
        for t, a in zip(self.method.retypes, self.result):
            arg = etree.SubElement(mth, 'ret')
            arg.attrib['type'] = t.__name__
            arg.text = repr(a)
        
        el.append(mth)
        
        etree.SubElement(el, 'repr').text = repr(self)
        etree.SubElement(el, 'short').text = str(self)
        
        etree.SubElement(el, 'highlighted').append(etree.fromstring(self.formatted()))
        
        return el

    def __str__(self):
        args = map(repr, self.result)

        s = "{self.klass}.{self.method!s}(".format(self=self)

        l = 100 - len(s)
        ar = []

        for a in args:
            if l - len(a) < 0:
                s += ', '.join(ar) + (', ' if ar else '') + '...)'
                break

            ar.append(a)
        else:
            s += ', '.join(ar) + ')'
        return s

    def __repr__(self):
        return "<-- {self.klass}.{self.method!s}({res})".format(**{
            'self': self,
            'res': ', '.join(map(repr, self.result)),
        })


class POPException(object):
    
    type = 'exception'
    
    def __init__(self, klass, properties, buffer):
        self.klass = klass
        self.properties = properties
    
    def toxml(self):
        return etree.Element('exception')


    def __repr__(self):
        return "<-x {self.klass}({properties})".format(**{
            'self': self,
            'properties': ', '.join(map(repr, self.properties)),
        })

