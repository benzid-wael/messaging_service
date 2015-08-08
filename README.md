# messaging_service

This is a simple messaging service written in Python that reads incoming messages from a RabbitMQ queue, and send out SMS and emails depending on message type.

# Features

* Flexible system
* Possibility to extend handler classes
* Possibility to define filter classes for handlers
* By default, the system pause sending SMS messages from 6 PM to 6 AM using WindowTimeFilter class

# TODO

* Python 3 support
* Refactoring of the messaging service (adding cli, etc.)
