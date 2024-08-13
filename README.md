# JSSG - Jtremesay's Static Site Generator

[![CI/CD](https://github.com/jtremesay/jssg/actions/workflows/main.yaml/badge.svg)](https://github.com/jtremesay/jssg/actions/workflows/main.yaml)

An ever evoluting thing that propulse [jtremesay.org](https://jtremesay.org).

## Specifications

It's not a generic static site generator. It's really tailored to my needs for [jtremesay.org](https://jtremesay.org). For most of its life, the code of jssg was merged with the content of jtremesay.org. I moved it to a separate repo because some [crazy people](https://github.com/jtremesay/jssg/issues/21#issue-2350427251) wanted to use it for profesisonal stuff[‽‽‽](https://en.wikipedia.org/wiki/Interrobang). 

My needs:
- I want to write my content on my computer with adapted tools, not in a shitty WSYIWYG editor in a web app
- I want the content in files in a git repository, not a in database
- I don't want to write HTML. The content should use markdown or whatever
- I need to be able to use a templating in the content. Sometime, I'm too lazy too write the content myself. It's really nice to have things like table automatically generated from a csv file or ect…
- Since everything is files and in git, use a CI/CD to build and deploy the site
- I don't need a backend or a database
- Fully static so easy to deploy / host on anything. FTP and RSYNC POWA!
- 2024-06-13: provide jssg as a django app instead of a django project so people can easily integrate it
- deployed on a docker swarm cluster on my kimsufi server, so I can be flex on what I use (just an containered nginx with a copy of the site)
- should be easy to use it locally (writting content / front stuff) and work on it

## History

JSSG was successively:

- a flask app (dynamic)
- a thing that use python + jinja + a very cerative use of makefile 
- a django project that can generate a fully static site + rss + processed static files
- the same, but with distill for the generation part

It's currently:

- a django app


In the future, it will become:

- TBD

## Installation

1. Install JSSG from the repo (no pypi package provided at this time):

```shell
python3 -m pip install --user https://github.com/jtremesay/jssg.git
```

2. Update `proj/settings.py` to add the JSSG:

```python3
INSTALLED_APPS = [
    ...,
    "jssg",
]
```

3. Update `proj/urls.py`:

```python
urlpatterns = [
    # TODO
    ...,
]
```

##  Usage

TODO. 

Be since I eat my own dog food, you can always look at how I use it in the jtremesay.org [repo](https://github.com/jtremesay/jtremesay.org).

## Configuration

TODO.