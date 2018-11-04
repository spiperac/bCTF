# bCTF Scoreboard System

Just another scoreboard system for hosting a CTF style games. 
We, at the BalCCon\dot\org, were using CTFd for quite some time ( inspiration for styling obvious), and we decided that we need some more features like:
easier challenge deployment, controll small set of docker containers, more interactions and informations feeded to players, etc... Thus bCTF came to existence.

## Getting Started

Installation is dead simple, and you have few options. You can run bCTF from host machine, or a docker. Or whatever you came up with.

### Prerequisites for host 

If you want to run it on your machine/server, you'll need to install:

```
python3
pip
docker - (optional)
```

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

## Running the tests

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


