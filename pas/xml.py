
from lxml import etree
from pas import shell

class Transformation(object):
    def __init__(self, stylesheet):
        self.path = stylesheet
        
        with open(stylesheet) as fh:
            self.document = etree.parse(fh)
        
        self.extensions = {}
    
    def registerFunction(self, namespace, func, name=None):
        if not name:
            name = func.__name__
        
        self.extensions[(namespace, name)] = func
    
    def transform(self, document_or_path, destination=None):
        if isinstance(document_or_path, basestring):
            with open(document_or_path) as fh:
                document = etree.parse(fh)
        else:
            try:
                document = etree.parse(document_or_path)
            except AttributeError:
                document = document_or_path
        
        transformation = etree.XSLT(self.document, extensions=self.extensions)
        transformed = transformation(document)
        
        if destination:
            with open(destination, 'w') as fh:
                fh.write(etree.tostring(transformed))
        
        return transformed
    
    def __call__(self, *args, **kwargs):
        return self.transform(*args, **kwargs)


def format(infile, outfile=None, local=True):
    run = shell.local if local else shell.remote
    outfile = outfile or infile
    
    run('XMLLINT_INDENT="\t" xmllint --format -o {outfile} {infile}'.format(
        infile=infile,
        outfile=outfile
    ))
    