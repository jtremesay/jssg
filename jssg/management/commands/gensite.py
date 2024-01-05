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
from typing import Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.urls import resolve, reverse

from jssg.models import Page, Post


def get_page(url: str, path: Optional[Path] = None) -> None:
    """Download a page an store the result.

    :param url: the url to retrieve
    :param path: the path to where store the retrieved content
        The path is derived from the url if not defined

    Note: the path will be prepended with settings.DIST_DIR
    """
    # Create the request object
    request = HttpRequest()
    request.META["HTTP_HOST"] = "jtremesay.org"
    request.method = "get"
    request.path = url
    request._get_scheme = lambda: "https"

    # Retrieve the view object associated with the url
    match = resolve(url)

    # Call the view
    response = match.func(request, *match.args, **match.kwargs)

    # Follow the redirection if needed
    if response.status_code in (301, 302):
        return get_page(response.url, path)

    if response.status_code != 200:
        raise ValueError(f"Unexpected status code {response.status_code} for url {url}")

    # Render the template if needed
    try:
        response.render()
    except AttributeError:
        ...

    # get the output path
    if path is None:
        path = settings.DIST_DIR / url[1:]
    else:
        path = settings.DIST_DIR / path

    # Create parent if needed and write the content
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
