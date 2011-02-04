"""
Measure management functions.
"""


import binascii
import errno
import glob
import os
import shutil
import xdrlib
from datetime import datetime

from pas import conf
from pas import tshark
from pas import shell
from pas import xml
from pas.conf import settings
from pas.conf import map_interfaces
from pas.conf import role
from pas.conf import stylesheet
from pas.parser import errors
from pas.parser import registry
from pas.parser import protocol

from lxml import etree


def select(name=None, basedir=None):
    """
    Scans the basedir (or the shared-measures directory defined in the
    settings) for directories and returns a choice based on different
    criteria:

     1. No directories are found; raise a RuntimeError
     2. The name is set; check if it was found and if so return it
     3. Only one directory is found; return the found directory
     4. Multiple directories are found; ask the user to pick one

    """
    name = name.rsplit('_', 2) if name else ()

    if not basedir:
        basedir = settings.PATHS['shared-measures'][0]

    # Get all files in the directory
    paths = os.listdir(basedir)

    # Rebuild the full path name
    paths = [(os.path.join(basedir, p), p.rsplit('_', 2)) for p in paths]

    # Filter out non-directories
    paths = [p for p in paths if os.path.isdir(p[0])]

    # If no entries remained, there are no test cases which can be run
    if not paths:
        raise RuntimeError("No test cases found.")

    # Check to see if chosen value exists in the available paths
    if name:
        for path in paths:
            if path[1] == name:
                return path[0], '_'.join(path[1])
        else:
            # Continue with selecting phase
            # @TODO: log
            print "The chosen path is not available."

    # There is not much to choose here
    if len(paths) == 1:
        # @TODO: log
        print "\nOnly one measure found: {0} ({1} at {2}).".format(*paths[0][1])
        path = paths[0]
        return path[0], '_'.join(path[1])

    # Present a list of choices to the user (paths must now contain more than
    # one item)
    print "\nMultiple measures found:\n"

    for i, (path, name) in enumerate(paths):
        index = '[{}]'.format(i)
        print '{0:>8s}: {1} ({2} at {3})'.format(index, *name)

    def valid(index):
        """
        Returns the correct entry in the paths list or asks for a correct
        value if the index is outside the boundaries.
        """
        try:
            path = paths[int(index)]
            return path[0], '_'.join(path[1])
        except (IndexError, ValueError):
            raise Exception("Enter an integer between 0 " \
                            "and {0}.".format(len(paths)-1))

    print
    return shell.prompt("Select a measure:", validate=valid)


def start(name):
    """
    Start a new named measure session in background on all interested hosts.

    The hosts are retrieved from the ROLES setting directive and a
    measure is started for each one.
    """
    dest = settings.PATHS['local-measures'][1]
    fltr = settings.CAPTURE_FILTER

    for host, interfaces in map_interfaces():
        with shell.workon(host):
            shell.remote('rm -rf {0} ; mkdir {0}'.format(dest), sudo=True)

            for i in interfaces:
                mname = '{0}.{1}'.format(name, i)
                tshark.start(mname, i, '{0}/{1}.raw'.format(dest, mname), fltr)


def stop(name):
    """
    Start a new named measure session in background on all interested hosts.

    As for the start function, the hosts are retrieved from the interfaces
    setting directive and the stop command issued on each one.
    """
    for host, interfaces in map_interfaces():
        with shell.workon(host):
            for i in interfaces:
                tshark.stop(name, i)


def kill():
    """
    Alias for tshark.kill
    """
    return tshark.kill()


def collect(name, overwrite=False):
    """
    Moves the relevant files to the shared directory by asking to empty the
    destination directory if needed.
    """

    ipaddr = '$(getip eth1)'
    name = "{0}_{1}".format(name, datetime.now().strftime('%Y-%m-%d_%H:%M'))

    guest_local = settings.PATHS['local-measures'][1]
    host_shared, guest_shared = settings.PATHS['shared-measures']
    destination = os.path.join(guest_shared, name, ipaddr)
    local = os.path.realpath(os.path.join(host_shared, name))

    try:
        if os.listdir(local):
            print "A directory with the same name ({0}) already " \
                  "exists.".format(name)

            if overwrite or shell.confirm("Would you like to replace it?"):
                shell.local('rm -rf {0}/*'.format(local))
            else:
                raise OSError(errno.ENOTEMPTY, "Directory not empty")
    except OSError as e:
        # If the file or directory don't exist, consume the exception
        if e.errno != errno.ENOENT:
            raise

    shell.remote('chown -R {0}:{0} {1}'.format(settings.VM_USER, guest_local),
                 sudo=True)
    shell.remote('mkdir -p "{0}/logs"'.format(destination))
    shell.remote('cp {0}/* "{1}"'.format(guest_local, destination))
    
    # Copy log files
    for logfile in settings.LOG_FILES:
        shell.remote('chown {0}:{0} "{1}" || true'.format(settings.VM_USER,
                     logfile), sudo=True)
        shell.remote('cp "{0}" "{1}/logs" || true'.format(logfile,
                     destination))


def toxml(name):
    """
    Converts all raw measure files for the given measure to xml using a remote
    tshark command.

    This will overwrite all already converted files with matching names.
    """
    host_shared, guest_shared = settings.PATHS['shared-measures']
    pattern = os.path.join(host_shared, name, "*", "*.raw")

    paths = glob.glob(pattern)
    paths = (guest_shared + path[len(host_shared):] for path in paths)

    with shell.workon(role('client')):
        for path in paths:
            tshark.pcaptoxml(path, path.replace('.raw', '.xml'),
                             settings.DISPLAY_FILTER)


def simplify(name, prettyprint=True):
    """
    Simplifies all the measure files in pdxml format of the given measure,
    converting them using the simplify XSL stylesheet. Old simplifications
    will be overwritten.

    If the prettyprint optional argument is True, the result will be formatted
    using the xmllint tool.
    """
    host_shared = settings.PATHS['shared-measures'][0]
    pattern = os.path.join(host_shared, name, "*", "*.xml")

    simplifier = xml.Transformation(stylesheet('simplify.xsl'))

    for source in glob.glob(pattern):
        if len(os.path.basename(source).split('.')) == 3:
            dest = source.replace('.xml', '.simple.xml')
            
            simplifier.parameters['loopback'] = str(int(source.endswith(
                                                        '.lo.xml')))
            simplifier.transform(source, dest)

            if prettyprint:
                xml.prettyprint(dest)


def decode(name, measure_case, prettyprint=False):
    """
    Decodes the simplified XML representation of the given measure by adding
    a "decoded" element to each packet containing a payload.

    The decoding is done using an XSL transformation coupled with an xslt
    python extension function which provides the "decoded" element given a
    payload text string.
    """
    host_shared = settings.PATHS['shared-measures'][0]
    types = os.path.join(measure_case, "types.py")
    
    types_registry = registry.TypesRegistry()
    types_registry.load('pas.conf.basetypes')
    
    try:
        types_registry.parse(types)
    except IOError:
        pass

    proto = protocol.MappingProtocol(types_registry)

    trans = xml.Transformation(stylesheet('decode.xsl'))

    def _decode(context, payload):
        """
        Decoding callback
        """
        
        # Convert the ascii representation back to binary data
        bin_payload = binascii.a2b_hex(''.join(payload))

        # Create an xdr stream with the payload
        stream = xdrlib.Unpacker(bin_payload)

        # Read the full frame length, it is not needed here
        _ = stream.unpack_uint()

        try:
            # Decode the remaining data as a full frame...
            # ...hoping that tcp hasn't split the message in more frames
            message = proto.decode_full_frame(stream)

            # @TODO: Logging, output and error management
        except EOFError as e:
            print "-" * 80
            print context, "Not enough data:", e
            print repr(stream.get_buffer())
            print "-" * 80
            return
        except errors.UnknownClass as e:
            print "-" * 80
            print context.context_node.attrib['timestamp'],
            print "Error while decoding packet:", e
            print binascii.b2a_hex(stream.get_buffer())
            print "-" * 80
            return
        except errors.UnknownMethod as e:
            print "-" * 80
            print context.context_node.attrib['timestamp'],
            print "Error while decoding packet:", e
            print binascii.b2a_hex(stream.get_buffer())
            print "-" * 80
            return
        except xdrlib.Error as e:
            print "-" * 80
            print context.context_node.attrib['timestamp'], e
            print repr(e.message)

            rest = stream.get_buffer()
            rem = stream.get_position()
            print binascii.b2a_hex(rest[rem:])
            print
            print repr(rest[rem:])
            print
            print str(rem) + "/" + str(_)
            print "*" * 80
            return

        # Convert the message to xml and send it back to the XSL template
        return message.toxml()

    trans.register_function('http://gridgroup.eia-fr.ch/popc',
                            _decode, 'decode')

    # Apply transformation to all simplified xml files
    pattern = os.path.join(host_shared, name, "*", "*.simple.xml")

    for source in glob.glob(pattern):
        dest = source.replace('.simple.xml', '.decoded.xml')
        trans.transform(source, dest)

        if prettyprint:
            xml.prettyprint(dest)


def report(name, measure_case):
    """
    Assembles all the acquired resources (such as source code, measures and
    log files) and generates an html page suitable for human interaction and
    analysis.
    """
    host_shared = settings.PATHS['shared-measures'][0]
    
    trans = xml.Transformation(stylesheet('report.xsl'))
    
    def sources(_):
        els = etree.Element('files')
        
        base = len(measure_case)+1
        
        for root, dirs, files in os.walk(measure_case):
            print root
            
            for f in files:
                if f.endswith(('.pyc', '.DS_Store', '.o')):
                    continue
                    
                path = os.path.join(root, f)
                name = path[base:]
                
                if name.startswith('build/'):
                    continue
                
                element = etree.SubElement(els, 'file')
                element.attrib['path'] = path
                element.attrib['name'] = name
    
        return els
    
    trans.register_function('http://gridgroup.eia-fr.ch/popc', sources)
    
    def logs(_):
        els = etree.Element('files')
        basel = len(os.path.join(settings.ENV_BASE, host_shared, name))
        base = os.path.join(settings.ENV_BASE, host_shared, name, '*.*.*.*', 'logs', '*')
        
        for log in glob.glob(base):
            element = etree.SubElement(els, 'file')
            element.attrib['path'] = log
            element.attrib['name'] = log[basel+1:]
    
        return els
    
    trans.register_function('http://gridgroup.eia-fr.ch/popc', logs)
    
    def format_stream(_, payload):
        """
        Stream formatting xslt callback
        """
        payload = ''.join(payload)
        
        def chunks(seq, n):
            """ Yield successive n-sized chunks from l.
            """
            for i in xrange(0, len(seq), n):
                yield seq[i:i+n]
        
        element = etree.Element('pre')
        
        payload = ' '.join(chunks(payload, 2))
        payload = ' '.join(chunks(payload, 12))
        payload = '\n'.join(chunks(payload, 104))
        
        for chunk in chunks(payload, 420):
            etree.SubElement(element, 'span').text = chunk
        
        return element
    
    trans.register_function('http://gridgroup.eia-fr.ch/popc', format_stream)
    
    
    class Highlighter(etree.XSLTExtension):
        def execute(self, context, self_node, input_node, output_parent):
            from pygments import highlight
            from pygments import lexers
            from pygments.formatters import HtmlFormatter
            
            # Highlight source text with pygments
            source = input_node.attrib['path']
            
            with open(source) as fh:
                code = fh.read()
            
            # Chose a lexer
            name = os.path.split(source)[1]
            
            if name == 'Makefile':
                lexer = lexers.BaseMakefileLexer()
            elif name.endswith('.py'):
                lexer = lexers.PythonLexer()
            elif name.endswith(('.cc', '.ph', '.h')):
                lexer = lexers.CppLexer()
            elif name.endswith(('.c',)):
                lexer = lexers.CLexer()
            else:
                lexer = lexers.TextLexer()
            
            # Highlight code
            highlighted = highlight(
                code, lexer, HtmlFormatter(cssclass="codehilite", style="pastie", linenos='table')
            )
            
            # Convert to xml
            root = etree.fromstring(highlighted)
            
            # Add to parent
            output_parent.extend(root)
    
    trans.register_element('http://gridgroup.eia-fr.ch/popc', 'highlighted', Highlighter())
    
    destination = os.path.join(host_shared, name, 'report')

    shutil.rmtree(destination, True)
    shell.local("mkdir -p {0}".format(destination))

    pattern = os.path.join(host_shared, name, "*", "*.decoded.xml")
    
    for source in glob.glob(pattern):
        base, measure = os.path.split(source)
        interface = measure.rsplit('.', 3)[1]
        ip = os.path.basename(base).replace('.', '-')
        dest = os.path.join(destination, '{0}_{1}.html'.format(ip, interface))
        trans.transform(source, dest)
        
        # Tidy
        tconf = "conf/tidy/tidy.conf"
        shell.local('tidy -config {1} -o {0} {0} || true'.format(dest, tconf))

    # Copy resources
    htdocs = os.path.join(os.path.dirname(conf.__file__), 'htdocs')
    
    #shell.local("ln -s {0} {1}".format(os.path.join(htdocs, 'styles'), 
    #   os.path.join(destination, 'styles')))
    #shell.local("ln -s {0} {1}".format(os.path.join(htdocs, 'images'), 
    #   os.path.join(destination, 'images')))
    #shell.local("ln -s {0} {1}".format(os.path.join(htdocs, 'scripts'),
    #   os.path.join(destination, 'scripts')))
    shutil.copytree(
        os.path.join(htdocs, 'styles'),
        os.path.join(destination, 'styles')
    )
    shutil.copytree(
        os.path.join(htdocs, 'images'),
        os.path.join(destination, 'images')
    )
    shutil.copytree(
        os.path.join(htdocs, 'scripts'),
        os.path.join(destination, 'scripts')
    )



