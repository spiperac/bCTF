# bCTF

bCTF is a scoreboard system for hosting and managing CTF style games. 
We, at the BalCCon.org, were using CTFd for quite some time ( that's why that ui looks familiar ...), and we decided that we need some more features like:
easier challenge deployment, controll small set of docker containers running challenges, more interactions and informations feeded to players, etc... Thus bCTF came to existence.

## Features

* CTFTime.org compatible scoreboard feed
* News & Events feed on home page
* CTF Timer ( start and stop time)
* Challenges Importer ( from .zip file)
* Challenges, categories, hints, flags, files ...
    * Challenge visibility can be toggled
    * Challenge files upload work out of box with S3, Dropbox, or bCTF host
    * First Blood! List showing teams who scored challenge first
    * Points degradation system - optional and off by default - can be configured from admin interface
* Live scoreboard
    * Graph with top 10 teams
    * Table with team names, gr/avatars, ranks, points, and (optional) country
* Account management system with captcha (captcha is #TODO atm)
    * You can ban/unban user accounts
* Pages interface for creating custom pages for eg. rules or faq ( auto-added to top menu)
* Supports Themes ( comes with few out of box)
* Admin interface
* Backup & Restore 
* Email support ( for registration, password resets, and optional account activation links)
* Beta themes customisation
* Fast and small on deps
    * bCTF is using django with minimal set of 3rd party libs
        * besides django, only pyyaml and django-countries are required
* Unit tests and selenium tests coverage
* Bootstrap 4
* Experimental docker controller interface where you can manage you challenge containers ( If you are not running bCTF inside docker)
    * Start/Stop/Restart/Pause/Reset container
    * Read logs
    * Delete containers
    * Create new containers from available images
    * Change docker host configuration

## Todo

* Plugins interface


## Getting Started

Installation is dead simple, and you have few options out of box. You can run bCTF from host machine, or a docker with included Dockerfile( comes with nginx). Or whatever you came up with.

## Deployment 


### Prerequisites for host machine

If you want to run it on your machine/server, you'll need to install:

* python3
* pip
* docker - (optional)


### Installing

After you got all initial requirements sorted out, there's few more things.

Required way to install python dependencies is to use virtualenv, like in this example.

So, go into your folder where you downloaded/cloned bCTF and type:

```
# Setup virtualenv and install dependencies

virtualenv env
source env/bin/activate
pip install -r requirements.txt

# Migrate
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8080

```

And point your browser of choice to http://localhost:8080

## Deployment with Docker

If you want to  use our supplied Dockerfile, keep in mind that it comes in production ready state, with Nginx running alongside with bCTF in supervisord inside container.

### Built With

docker build -t bCTF .

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

* **S. Piperac ( badarg) ** - *Initial work* - [@0xbadarg](https://twitter.com/0xbadarg)

See also the list of [contributors](https://github.com/spiperac/bctf/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


