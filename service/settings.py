# -*- coding: utf-8 -*-

DEBUG = False

# SMTP authentication information
EMAIL_HOST = 'mailtrap.io'
EMAIL_PORT = '2525'
EMAIL_HOST_USER = '32897a27018e9d185'
EMAIL_HOST_PASSWORD = '51cc1e99f8a129'


MESSAGE_QUEUE = {
    'HOST': 'localhost',
    'NAME': 'messaging_service',
    'handlers': {
        'sms': {
            'class': 'service.handlers.SMSHandler',
            'filter': {
                'class': 'service.handlers.filters.WindowTimeFilter',
                'extra': {
                    'from_time': '18:00',
                    'to_time': '06:00',
                }
            },
        },
        'email': {
            'class': 'service.handlers.EmailHandler',
        },
    },
}
