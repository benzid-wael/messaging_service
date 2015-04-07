# -*- coding: utf-8 -*-

from service import settings as global_settings


def load_class(name):
    """
    load the class defined by dotted path if possible, or raise an error.

    :raises ImportError: raise ImportError if we can not load the base module
    :raises AttributeError: raise AttributeError if the base module does not
    have the requested class.
    """
    parts = name.split('.')
    module = __import__('.'.join(parts[0:-1]), globals(), locals(),
                        [parts[-1]])
    return getattr(module, parts[-1])


def load_handlers(settings=None):
    """ Load an initialized copy of message handlers. """
    handlers = {}
    if not settings:
        settings = global_settings
    for message_type, handler_cfg in settings.MESSAGE_QUEUE['handlers'].items():
        handler_cls = load_class(handler_cfg['class'])
        handler = handler_cls()
        filtler_config = handler_cfg.get('filter', None)
        if filtler_config:
            filter_cls = load_class(filtler_config['class'])
            filter_kwargs = filtler_config.get('extra', {})
            filter_instance = filter_cls(**filter_kwargs)
            handler.filter = filter_instance
        handlers[message_type] = handler
    return handlers
