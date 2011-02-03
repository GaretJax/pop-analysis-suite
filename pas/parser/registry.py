import sys
import os
import imp

from pas.parser import errors


current_registry = None


class TypesRegistry(object):
    
    def __init__(self):
        self.classes = dict()
        self.exceptions = dict()
    
    def register_class(self, cls):
        self.classes[cls.id] = cls
    
    def register_exception(self, exc):
        self.exceptions[exc.id] = exc
    
    def get_class(self, classid):
        try:
            return self.classes[classid]
        except KeyError:
            raise errors.UnknownClass(classid)
    
    def get_exception(self, excid):
        try:
            return self.exceptions[excid]
        except KeyError:
            raise errors.UnknownException(excid)
    
    def load(self, module_name):
        global current_registry
        
        current_registry = self
        __import__(module_name)
        current_registry = None
    
    def parse(self, module_path):
        global current_registry
        
        path, module_file = os.path.split(module_path)
        module_name = module_file.rsplit('.', 1)[0]
        
        current_registry = self
        imp.load_source(module_name, module_path)
        current_registry = None

