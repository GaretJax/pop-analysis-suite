

class UnknownClass(ValueError):
    """
    Raised when an unknown class id is encountered.
    """
    def __init__(self, classid):
        super(UnknownClass, self).__init__()
        self.classid = classid
    
    def __str__(self):
        return "Unknown class: {}".format(self.classid)


class UnknownException(UnknownClass):
    """
    Raised when an unknown exception id is encountered.
    """
    pass


class UnknownMethod(ValueError):
    """
    Raised when an unknown method id is encountered.
    """
    def __init__(self, klass, methodid):
        super(UnknownMethod, self).__init__()
        self.klass = klass
        self.methodid = methodid

    def __str__(self):
        return "Unknown method for class {0!s}: {1}".format(self.klass,
                                                            self.methodid)