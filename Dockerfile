FROM python:3.6-alpine

# File Author / Maintainer
MAINTAINER badarg <spiperac@denkei.org>

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN chmod +x /app/docker-entrypoint.sh

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libjpeg-turbo-dev jpeg mariadb-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps libjpeg-turbo-dev jpeg-dev jpeg mysql-client \
    && apk del .build-deps

ENV DJANGO_SETTINGS_MODULE bctf.settings.production

RUN python manage.py collectstatic --noinput
RUN rm -rf ./static/

EXPOSE 31337
# CMD ["/usr/local/bin/gunicorn", "--chdir", "/app/", "--workers=4", "bctf.wsgi", "-b", "0.0.0.0:8000"]

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]