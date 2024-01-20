# JSSG - Jtremesay's Static Site Generator

[![CI/CD](https://github.com/jtremesay/jssg/actions/workflows/main.yaml/badge.svg)](https://github.com/jtremesay/jssg/actions/workflows/main.yaml)

The thing that propulse [jtremesay.org](https://jtremesay.org).

Today, it's a django app that can generate a static website with Vite & Typescript integration.

## Bootstrap

```shell
$ git clone https://github.com/jtremesay/jtremesay.org.git
$ cd jtremesay.org
$ direnv allow
$ npm install
$ pip install -Ur requirements.txt
```

## Dev

You need to run BOTH npm and the django server. Npm will transpile the typescript code on the fly and provide hot reloading.

Note: if you use `direnv`, the environment variable `DJANGO_DEBUG` is set to `true`. No need to prefix the commands with `DJANGO_DEBUG=true`.

```shell
$ DJANGO_DEBUG=true npm run dev
```

```shell
$ DJANGO_DEBUG=true ./manage.py runserver
```

## Prod

Note: if you use `direnv`, the environment variable `DJANGO_DEBUG` is set to `true`. You must then prefix tho following commands with `DJANGO_DEBUG=false`.

```shell
$ npm run build
$ ./manage.py distill-local --collectstatic --force dist
```

Or, if you prefer docker:

```shell
$ docker build -t jssg .
```
