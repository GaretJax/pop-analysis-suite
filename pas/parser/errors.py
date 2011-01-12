

class UnknownClass(ValueError):
    def __init__(self, classid):
        self.classid = classid
    
    def __str__(self):
        return "Unknown class: {}".format(self.classid)


class UnknownException(UnknownClass):
    pass


class UnknownMethod(ValueError):
    def __init__(self, klass, methodid):
        self.klass = klass
        self.methodid = methodid

    def __str__(self):
        return "Unknown method for class {0!s}: {1}".format(self.klass, self.methodid)