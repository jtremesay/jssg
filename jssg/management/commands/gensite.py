from pathlib import Path
from pprint import pprint
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpRequest
from django.test import Client, RequestFactory
from django.urls import resolve, reverse

from jssg.models import Page, Post
from jssg.views import PageView, PostView


def get_page(url: str, path: Optional[Path] = None) -> None:
    match = resolve(url)
    request = HttpRequest()
    request.META["HTTP_HOST"] = "jtremesay.org"
    request.method = "get"
    request.path = url
    request._get_scheme = lambda: "https"
    response = match.func(request)
    if response.status_code in (301, 302):
        return get_page(response.url, path)

    assert response.status_code == 200

    try:
        response.render()
    except AttributeError:
        ...

    if path is None:
        path = settings.DIST_DIR / url[1:]
    else:
        path = settings.DIST_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(response.content)


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_page("/", "index.html")
        get_page("/atom.xml")
        for page in Page.load_glob():
            if page.slug == "index":
                continue

            url = reverse("page", args=(page.slug,))
            get_page(url)

        for post in Post.load_glob():
            url = reverse("post", args=(post.slug,))
            get_page(url)
