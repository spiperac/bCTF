# Installation and Deployment

bCTF is simple as posible to install. It's also very light on system package dependencies.

## Host Prerequisites

You will need following available on your host machine:

* Python 3.4+
* Pip
* (optional) Virtualenv - recommended
* (optional) Docker - it's optional, but if you have it, you'll be able to controll challenge containers from bCTF administration panel.

## Host Installation

This is suitable for test/local runs.
If you wan't to run bCTF from your virtual machine, make sure you have items described in prerequisites installed.
Go to your project root, where you cloned bCTF repository, and run following:

* [/opt/bctf/]$ virtualenv env
* [/opt/bctf/]$ source env/bin/activate
* [/opt/bctf/]$ python manage.py migrate
* [/opt/bctf/]$ python manage.py runserver 127.0.0.1:8000

Then open your browser and point to [http://localhost:8000](http://localhost:8000) and you will see bCTF Installation and Setup page.

### Production changes

For production, you will only have to export DJANGO_SETTINGS_MODULE environment variable to 'bctf.settings.production', so django can know that you are running in production,
and use corresponding settings.

* [/opt/bctf/]$ export DJANGO_SETTINGS_MODULE=bctf.settings.production
* [/opt/bctf/]$ python manage.py runserver 127.0.0.1:8000


## Docker

If you want to run it inside docker, keep in mind that Dockerfile that comes with repository also includes instances of nginx running insade and serving application and static files.
Both nginx and bCTF are running from supervisor inside docker.

To get it running:

* [/opt/bctf/]$ docker build -t bctf .
* [/opt/bctf/]$ docker run -p 80:80 bctf 

Then open your browser and point to [http://localhost:8000](http://localhost:8000) and you will see bCTF Installation and Setup page.
