Flaskberry
==========

A simple web application to manage your Raspberry Pi.

Features:
 - shutdown and reboot
 - mount and unmout disks, USB drives, etc.
 - simplistic HTML movie player

Please bear in mind, that by running Flaskberry you are exposing an
unsecured power off switch to your Raspberry Pi to the network and
possibly to the whole internet when connected. Commands are executed
via sudo with with root privileges which is another potential security
problem. Please use Flaskberry only if your not storing any valuable
information on it.

Flaskberry is written in Python an uses the [Flask][1] framework.

To run Flaskberry you need Python 2.7, Flask 0.10, [psutil][2], a
web-server and some WSGI-Container to run the application in and ideally
something for monitoring.
I recommend [nginx][3], [uWSGI][4] or [gunicorn][5] and [supervisor][6].
There are sample configurations in the directory examples/ which assume
the application (and the file you are reading now) is stored in
/home/pi/flaskberry.

Rename settings.example.py to settings.py, change the SECRET_KEY in to
something random and adapt other options to your needs.

The application itself is released under the MIT License.
It ships with a copy of [Twitter Bootstrap][7], which is licensed under
the Apache License v2.0. Twitter Bootstrap contains Icons from
Glyphicons Free, licensed under CC BY 3.0.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.

2013-2015, Rupert Angermeier


[1]: http://flask.pocoo.org/
[2]: https://code.google.com/p/psutil/
[3]: http://nginx.org/
[4]: http://projects.unbit.it/uwsgi/
[5]: http://gunicorn.org/
[6]: http://supervisord.org/
[7]: http://twitter.github.com/bootstrap/
