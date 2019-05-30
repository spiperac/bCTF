# bCTF

bCTF is a scoreboard system for hosting and managing security CTF competitions/games. 
We, at the BalCCon.org, were using CTFd for quite some time ( that's why that ui looks familiar ...), and we decided that we need some more features like:
rest api, easier challenge deployment, controll small set of docker containers running challenges, more interactions and informations feeded to players, etc... Thus bCTF came to existence.

## Features

* REST API
* News & Events feed on home page
* CTF Timer - Start & Stop timer
* Challenges Importer/Exporter ( from/to .zip file)
* Challenges, categories, hints, flags, files ...
    * Challenge visibility can be toggled
    * Challenge files upload work out of box with S3, Dropbox, or bCTF host
    * First Bloods! List showing teams who scored challenge first
    * Points degradation system - optional and off by default - can be configured from admin interface
* Live scoreboard
    * Graph with top 10 teams
    * Table with team names, gr/avatars, ranks, points, and (optional) country
* Account management system with captcha (captcha is #TODO atm)
    * You can ban/unban user accounts
    * Upgrade other accounts to staff/admin
* Pages interface for creating custom pages for eg. rules or faq ( auto-added to top menu)
* Supports Themes ( comes with few out of box)
* Supports Plugins ( comes with few out of box)
* Super easy to develop custom theme.
* Super easy to develop custom plugin.
* CTFTime.org compatible scoreboard feed (Plugin enabled out of box)
* Admin interface
* Backup & Restore 
* Email support ( for registration, password resets, and optional account activation links)
* Fast and small on deps
    * bCTF is using django with minimal set of 3rd party libs
        * besides django, only drf and django-countries are required
* Unit tests and selenium tests coverage
* Bootstrap 4
* Experimental docker controller interface where you can manage you challenge containers ( If you are not running bCTF inside docker)
    * Start/Stop/Restart/Pause/Reset container
    * Read logs
    * Delete containers
    * Create new containers from available images
    * Change docker host configuration

## Todo

* Vue.js front as an alternative to django-templates.


## Getting Started

Installation is dead simple, and you have few options out of box. You can run bCTF from host machine, or a docker with included Dockerfile( comes with nginx). Or whatever you came up with.

## Deployment 


### Prerequisites for host machine

If you want to run it on your machine/server, you'll need to install:

* python3
* pip
* docker - (optional)


### Installing

After you got all initial system requirements sorted out, there's few more things.

Go into your folder where you downloaded/cloned bCTF and type:

```
pip install -r requirements.txt

# Migrate and run!
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8080
```

Or, if you want to use virtualenv (which is recommented!) do this:

```
# Setup virtualenv and install dependencies

virtualenv env
source env/bin/activate
pip install -r requirements.txt

# Migrate and run!
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8080

```

And point your browser of choice to http://localhost:8080

## Deployment with Docker

If you want to  use our supplied Dockerfile, keep in mind that it comes in production ready state, with Nginx running alongside with bCTF in supervisord inside container.

### Built With

docker build -t bCTF .

## Deployment with Docker Compose

If you want to  use our supplied docker-compose.yml, copy .env.example to .env and change desired variables like db settings.
Once you are done, you can run docker-compose up, which should bring up db, web, and bctf-app containers.

* Note: In docker-compose file, containers are linked together in a isolated network, so, in order for bctf-app to see
a mysql server ( for example), you will have to specify containers name in .env DB_HOST instead of IP address.
Which in this case would be "db".


### Run 
docker run -p 80:80 bCTF

## Running tests

Run:
```
python3 manage.py test
```

## Contributing

Pull requests and bug reports are more than welcome. As for the coding standard, well, follow PEP8, except no body cares about line length. 

## Authors

* **S. Piperac - [@0xbadarg](https://twitter.com/0xbadarg)

See also the list of [contributors](https://github.com/spiperac/bctf/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


