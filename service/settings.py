# -*- coding: utf-8 -*-

MESSAGE_QUEUE = {
    'HOST': 'localhost',
    'NAME': 'messaging_service',
    'handlers': {
        'sms': {
            'class': 'service.handlers.SMSHandler',
            'filter': {
                'class': 'service.handlers.filters.WindowTimeFilter',
                'extra': {
                    'from': '18:00',
                    'to': '06:00',
                }
            },
        },
        'email': {
            'class': 'service.handlers.EmailHandler',
        },
    },
}
