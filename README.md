# messaging_service

This is a simple messaging service written in Python that reads incoming messages from a RabbitMQ queue, and send out SMS and emails depending on message type.

# Features

* Flexible system
* Possibility to extend handler classes
* Possibility to define filter classes for handlers
* By default, the system pause sending SMS messages from 6 PM to 6 AM using WindowTimeFilter class
* Sending emails via mailtrap
* Simulation of sending SMS (print it out to console)

# TODO

* Python 3 support
* Refactoring of the messaging service (adding cli, etc.)
* Support of different SMS APIs such as Twilio, BulkSMS, etc.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/benzid-wael/messaging_service/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

