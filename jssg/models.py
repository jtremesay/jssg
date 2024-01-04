import datetime
from io import StringIO
from pathlib import Path
from typing import Iterator, Optional

import markdown2
from django.conf import settings
from django.template import Context, Template
from django.utils.text import slugify


class Document:
    BASE_DIR = settings.CONTENT_DIR

    """A document

    A text with some metadata

    This is a base class for more specialized document types
    """

    def __init__(self, content: str, **metadata) -> None:
        self.content = content
        self.metadata = dict(metadata)
        self.path = metadata["path"]

    @property
    def content_md(self):
        return markdown2.markdown(
            Template(self.content).render(
                Context(
                    {
                        "posts": sorted(
                            Post.load_glob(), key=lambda p: p.timestamp, reverse=True
                        )
                    }
                )
            ),
            extras=["fenced-code-blocks"],
        )

    @classmethod
    def load(cls, path: Path) -> "Document":
        """Load a document

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

    @classmethod
    def load_glob(
        cls, path: Optional[Path] = None, glob: str = "*.md"
    ) -> Iterator["Document"]:
        """Load multiple document

        :param path: The base path
        :param glob: The glob pattern
        :return: The documents that match the pattern
        """
        if path is None:
            path = cls.BASE_DIR

        if path is None:
            raise RuntimeError("No path and no self.BASE_DIR defined")

        return map(cls.load, path.glob(glob))


class Page(Document):
    """A webpage, with a title and some content"""

    BASE_DIR = settings.PAGES_DIR

    def __init__(self, content: str, **metadata) -> None:
        super().__init__(content, **metadata)
        self.title = metadata["title"]
        try:
            self.slug = metadata["slug"]
        except KeyError:
            self.slug = slugify(self.title)

    @classmethod
    def load_page_with_slug(cls, slug: str) -> "Page":
        return next(filter(lambda p: p.slug == slug, cls.load_glob()))

    @classmethod
    def load_glob(
        cls, path: Optional[Path] = None, glob: str = "*.md"
    ) -> Iterator["Page"]:
        return super().load_glob(path, glob)


class Post(Page):
    """A webblog post"""

    BASE_DIR = settings.POSTS_DIR

    def __init__(self, content: str, **metadata) -> None:
        super().__init__(content, **metadata)
        self.timestamp = datetime.datetime.fromisoformat(metadata["date"])

    @classmethod
    def load_glob(
        cls, path: Optional[Path] = None, glob: str = "*.md"
    ) -> Iterator["Post"]:
        return super().load_glob(path, glob)
