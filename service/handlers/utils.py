# -*- coding: utf-8 -*-


def load_class(name):
    """
    load the class defined by dotted path if possible, or raise an error.
    
    :raise ImportError: raise ImportError if we can not load the base module
    :raise AttributeError: raise AttributeError if the base module does not
    have the requested class.
    """
    parts = name.split('.')
    module = __import__('.'.join(parts[0:-1]), globals(), locals(),
                        [parts[-1]])
    return getattr(module, parts[-1])
    
