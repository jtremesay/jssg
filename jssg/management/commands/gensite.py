# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2024 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path
from pprint import pprint
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.urls import resolve, reverse

from jssg.models import Page, Post


def get_page(url: str, path: Optional[Path] = None) -> None:
    match = resolve(url)
    request = HttpRequest()
    request.META["HTTP_HOST"] = "jtremesay.org"
    request.method = "get"
    request.path = url
    request._get_scheme = lambda: "https"
    response = match.func(request, *match.args, **match.kwargs)
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
        get_page(reverse("index"), "index.html")
        get_page(reverse("atom_feed"))
        for page in Page.load_glob():
            if page.slug == "index":
                continue
            get_page(reverse("page", args=(page.slug,)))
        for post in Post.load_glob():
            get_page(reverse("post", args=(post.slug,)))
