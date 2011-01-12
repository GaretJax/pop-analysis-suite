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
        basedir = settings.paths['shared-measures'][0]

    # Get all files in the directory
    paths = os.listdir(basedir)

    # Rebuild the full path name
    paths = [(os.path.join(basedir, p), p.rsplit('_', 2)) for p in paths]

    # Filter out non-directories
    paths = filter(lambda p: os.path.isdir(p[0]), paths)

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

    The hosts are retrieved from the interfaces setting directive and a
    measure is started for each one.
    """
    dest = settings.paths['local-measures'][1]
    fltr = settings.capture_filter

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

    ip = '$(getip eth1)'
    name = "{0}_{1}".format(name, datetime.now().strftime('%Y-%m-%d_%H:%M'))

    guest_local = settings.paths['local-measures'][1]
    host_shared, guest_shared = settings.paths['shared-measures']
    destination = os.path.join(guest_shared, name, ip)
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

    shell.remote('chown -R {0}:{0} {1}'.format(settings.vm_user, guest_local),
                 sudo=True)
    shell.remote('mkdir -p "{0}"'.format(destination))
    shell.remote('cp {0}/* "{1}"'.format(guest_local, destination))


def toxml(name):
    """
    Converts all raw measure files for the given measure to xml using a remote
    tshark command.

    This will overwrite all already converted files with matching names.
    """
    host_shared, guest_shared = settings.paths['shared-measures']
    pattern = os.path.join(host_shared, name, "*", "*.raw")

    paths = glob.glob(pattern)
    paths = (guest_shared + path[len(host_shared):] for path in paths)

    with shell.workon(role('client')):
        for path in paths:
            tshark.pcaptoxml(path, path.replace('.raw', '.xml'))


def simplify(name, format=True):
    """
    Simplifies all the measure files in pdxml format of the given measure,
    converting them using the simplify XSL stylesheet. Old simplifications
    will be overwritten.

    If the format optional argument is True, the result will be formatted
    using the xmllint tool.
    """
    host_shared = settings.paths['shared-measures'][0]
    pattern = os.path.join(host_shared, name, "*", "*.xml")

    tr = xml.Transformation(stylesheet('simplify.xsl'))

    for source in glob.glob(pattern):
        if not source.endswith('.simple.xml'):
            dest = source.replace('.xml', '.simple.xml')
            tr.transform(source, dest)

            if format:
                xml.format(dest)


def decode(name, format=False):
    """
    Decodes the simplified XML representation of the given measure by adding
    a "decoded" element to each packet containing a payload.

    The decoding is done using an XSL transformation coupled with an xslt
    python extension function which provides the "decoded" element given a
    payload text string.
    """
    types_registry = registry.TypesRegistry()
    types_registry.load('pas.conf.basetypes')

    proto = protocol.MappingProtocol(types_registry)

    trans = xml.Transformation(stylesheet('decode.xsl'))

    def _decode(context, payload):
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
            print context.context_node.attrib['timestamp'], "Error while decoding packet:", e
            print binascii.b2a_hex(stream.get_buffer())
            print "-" * 80
            return
        except xdrlib.Error as e:
            print "-" * 80
            print context.context_node.attrib['timestamp'], e
            print repr(e.message)

            r = stream.get_buffer()
            rem = stream.get_position()
            print binascii.b2a_hex(r[rem:])
            print
            print repr(r[rem:])
            print
            print str(rem) + "/" + str(_)
            print "*" * 80
            return

        # Convert the message to xml and send it back to the XSL template
        return message.toxml()

    trans.registerFunction('http://gridgroup.eia-fr.ch/popc', _decode, 'decode')

    # Apply transformation to all simplified xml files
    host_shared = settings.paths['shared-measures'][0]
    pattern = os.path.join(host_shared, name, "*", "*.simple.xml")

    for source in glob.glob(pattern):
        dest = source.replace('.simple.xml', '.decoded.xml')
        trans.transform(source, dest)

        if format:
            xml.format(dest)


def report(name):
    """
    Assembles all the acquired resources (such as source code, measures and
    log files) and generates an html page suitable for human interaction and
    analysis.
    """
    
    trans = xml.Transformation(stylesheet('report.xsl'))
    
    def format_stream(context, payload):
        payload = ''.join(payload)
        
        def chunks(l, n):
            """ Yield successive n-sized chunks from l.
            """
            for i in xrange(0, len(l), n):
                yield l[i:i+n]
        
        el = etree.Element('pre')
        
        payload = ' '.join(chunks(payload, 2))
        payload = ' '.join(chunks(payload, 12))
        payload = '\n'.join(chunks(payload, 104))
        
        for b in chunks(payload, 420):
            etree.SubElement(el, 'span').text = b
        
        return el
    
    trans.registerFunction('http://gridgroup.eia-fr.ch/popc', format_stream)
    
    host_shared = settings.paths['shared-measures'][0]
    destination = os.path.join(host_shared, name, 'report')

    shutil.rmtree(destination, True)
    shell.local("mkdir -p {0}".format(destination))

    pattern = os.path.join(host_shared, name, "*", "simple.lo.decoded.xml")

    for source in glob.glob(pattern):
        dest = os.path.join(destination, 'index.html')
        trans.transform(source, dest)
        
        # Tidy
        shell.local('tidy -config conf/tidy/tidy.conf -o {0} {0} || true'.format(dest))
        
        # break after the first one
        # @TODO: Assemble all resources
        break

    # Copy resources
    htdocs = os.path.join(os.path.dirname(conf.__file__), 'htdocs')
    
    shutil.copytree(os.path.join(htdocs, 'styles'), os.path.join(destination, 'styles'))
    shutil.copytree(os.path.join(htdocs, 'images'), os.path.join(destination, 'images'))
    shutil.copytree(os.path.join(htdocs, 'scripts'), os.path.join(destination, 'scripts'))



