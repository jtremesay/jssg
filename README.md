# JSSG - Jtremesay's Static Site Generator

[![CI/CD](https://github.com/jtremesay/jssg/actions/workflows/main.yaml/badge.svg)](https://github.com/jtremesay/jssg/actions/workflows/main.yaml)

The thing that propulse [jtremesay.org](https://jtremesay.org).

Today, it's a django app that can generate a static website.

## Bootstrap

```shell
$ git clone https://github.com/jtremesay/jtremesay.org.git
$ cd jtremesay.org
$ direnv allow
$ pip install -Ur requirements.txt
```

## Dev

```shell
$ DJANGO_DEBUG=true ./manage.py runserver
```

## Prod

```shell
$ ./manage.py collectstatic --no-input
$ ./manage.py gensite
```

Or, if you prefer docker

```shell
$ docker build -t jssg .
```
