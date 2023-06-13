try:
    import filters
except ImportError:
    from pathlib import Path
    import sys

    sys.path.insert(0, str(Path(__file__).parent.resolve()))
    import filters


AUTHOR = "Jonathan Tremesaygues"
SITENAME = "jtremesay.org"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "fr"

STATIC_PATHS = ["static"]
THEME = "theme"
PLUGINS = ["jinja2content"]
JINJA_FILTERS = {"read_csv": filters.read_csv}


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = None

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
