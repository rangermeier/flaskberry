Flaskberry
==========

A simple web application to manage your Raspberry Pi.

Features
--------

 - shutdown and reboot
 - mount and unmout disks, USB drives, etc.
 - simplistic HTML movie player, remote controllable via WebSockets

**Warning** Please bear in mind, that by running Flaskberry you are exposing an
unsecured power off switch to your Raspberry Pi to the network and
possibly to the whole internet when connected. Commands are executed
via sudo with with root privileges which is another potential security
problem. Please use Flaskberry only if your not storing any valuable
information on it.

Flaskberry is written in Python an uses the [Flask][1] framework.

Installation
------------

To run Flaskberry you need Python 2.7, [nginx][4] > 1.4, [gunicorn][5] and
[supervisor][6]. At this point of time Raspbian ships only nginx 1.2.x, so
you'll have to [compile an up-to-date version][7] or find a deb-package.
The other packages can be installed with apt:

    sudo apt-get install python gunicorn supervisor

Next install required Python packages:

    sudo pip install -r requirements.txt
    
There are sample configurations for nginx and supervisor in the directory
`examples/` which assume the application (and the file you are reading now)
is stored in `/home/pi/flaskberry`. Copy them to `/etc/nginx/conf.d/` 
respectively to `/etc/supervisor/conf.d/` and adapt them to your needs.

Finally rename `flaskberrs/settings.example.py` to `flaskberry/settings.py`,
change the SECRET_KEY to something random and adapt other options.

Now restart supervisor and nginx. If everything is configured correctly you
should be able to open flaskberry in your web browser with the IP address of
your raspberry.

    sudo service supervisor restart
    sudo service nginx restart

Licence
-------

The application itself is released under the MIT License.

It ships with a copy of [Twitter Bootstrap][8], which is licensed under
the Apache License v2.0. Twitter Bootstrap contains Icons from
Glyphicons Free, licensed under CC BY 3.0.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.

2013-2015, Rupert Angermeier


[1]: http://flask.pocoo.org/
[2]: https://code.google.com/p/psutil/
[3]: https://github.com/miguelgrinberg/Flask-SocketIO
[4]: http://nginx.org/
[5]: http://gunicorn.org/
[6]: http://supervisord.org/
[7]: http://www.raspberrypi.org/forums/viewtopic.php?p=500185&sid=3644ca4c9190bc684ca2bb4a270df86e#p500185
[8]: http://twitter.github.com/bootstrap/
