# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2024 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import datetime
from io import StringIO
from pathlib import Path
from typing import Iterator, Mapping

import markdown2
from django.apps import apps
from django.template import Context, Template
from django.utils.text import slugify


class Document:
    """A document.

    A text with some metadata

    This is a base class for more specialized document types
    """

    def __init__(self, content: str, **metadata: Mapping[str, str]) -> None:
        """Create a new document.

        :param content: The content (body) of the document
        :param metadata: Associated metadata
        """
        self.content = content
        self.metadata = dict(metadata)
        self.path = metadata["path"]

    @property
    def content_md(self) -> str:
        """Render the content as markdown to html.

        Note: the content will be processed by the django template engine
        before being converted to html

        :return: the rendered document
        """
        return markdown2.markdown(
            Template(self.content).render(
                Context(
                    {
                        "posts": sorted(
                            find_posts(),
                            key=lambda p: p.timestamp,
                            reverse=True,
                        )
                    }
                )
            ),
            extras=["fenced-code-blocks", "tables"],
        )

    @classmethod
    def load(cls, path: Path) -> "Document":
        """Load a document.

        :param path: Path to the document
        :return: The loaded document
        """
        metadata = {}
        content = StringIO()

        with path.open() as f:
            # States:
            # 0: search the metadata start block
            # 1: parse the metadata
            # 2: parse the content
            state = 0
            for line in f:
                if state == 0:
                    # Search the metadata start block
                    # The metadata start block is expected to be on the first line
                    if line.rstrip() == "---":
                        # Metadata start block found
                        state = 1
                    else:
                        # Metadata start block not found, abort
                        break
                elif state == 1:
                    if line.rstrip() == "---":
                        # Metadata end block found
                        state = 2
                    else:
                        # Parse a metadata key value pair
                        key, value = map(str.strip, line.split(":", maxsplit=1))
                        metadata[key] = value
                else:
                    # Read the content
                    content.write(line)

        if state == 0:
            # Empty document or document not starting by a metadata block
            raise ValueError(
                f"Document {path.resolve()} doesn't start with a meta-data block"
            )
        elif state == 1:
            # Metadata end block not found
            raise ValueError(
                f"Document {path.resolve()}'s meta-data block doesn't have an end"
            )

        metadata["path"] = path

        return cls(content=content.getvalue(), **metadata)


class Page(Document):
    """A webpage, with a title and some content."""

    def __init__(self, content: str, **metadata) -> None:
        """Create a new page.

        :param content: The content (body) of the page
        :param metadata: Associated metadata
        """
        super().__init__(content, **metadata)
        self.title = metadata["title"]
        try:
            self.slug = metadata["slug"]
        except KeyError:
            self.slug = slugify(self.title)


class Post(Page):
    """A webblog post."""

    def __init__(self, content: str, **metadata) -> None:
        """Create a new post.

        :param content: The content (body) of the page
        :param metadata: Associated metadata
        """
        super().__init__(content, **metadata)
        self.timestamp = datetime.datetime.fromisoformat(metadata["date"])


def find_documents(sub_path: Path, doc_class: type[Document]) -> Iterator[Document]:
    """Find all the documents in the apps."""
    for app in apps.get_app_configs():
        path = Path(app.path) / "content" / sub_path
        for doc_path in path.glob("*.md"):
            yield doc_class.load(doc_path)


def find_pages() -> Iterator[Post]:
    """Find all the posts in the apps."""
    yield from find_documents(Path("pages"), Page)


def find_posts() -> Iterator[Post]:
    """Find all the posts in the apps."""
    yield from find_documents(Path("posts"), Post)


def get_page(slug: str) -> Page:
    """Get a page by its slug."""
    for page in find_pages():
        if page.slug == slug:
            return page

    raise ValueError(f"Page {slug} not found")


def get_post(slug: str) -> Post:
    """Get a post by its slug."""
    for post in find_posts():
        if post.slug == slug:
            return post

    raise ValueError(f"Post {slug} not found")
