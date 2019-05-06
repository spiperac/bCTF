#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"/..


apt update && apt install docker python3 python3-pip
pip install -r "$DIR/requirements.txt"
python manage.py makemigrations && python manage.py migrate

