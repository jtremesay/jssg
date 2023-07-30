# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2023 Jonathan Tremesaygues
#
# jssg.py
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
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime as DateTime
from distutils.dir_util import copy_tree
from io import StringIO
from pathlib import Path
from typing import Any, Generator, Iterable, Optional
from urllib.parse import urlparse

from docutils.core import publish_parts
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from jinja2.environment import Environment
from unidecode import unidecode

logger = logging.getLogger(__name__)


def docutils_filter(value: str) -> str:
    return publish_parts(value, writer_name="html5")["body"]


def slugify(title: str) -> str:
    def step1(title: str):
        for c in title:
            if c.isalpha():
                yield c.lower()
            elif c.isdigit():
                yield c
            elif c == " ":
                yield "_"

    def step2(title: str):
        prev = None
        for c in step1(title):
            if c == "_" and prev == "_":
                continue

            yield c
            prev = c

    return "".join(step2(unidecode(title)))


@dataclass
class Config:
    site_name: str
    site_url: str
    author_name: str


@dataclass
class Document:
    metadata: dict[str, str]
    content_rst: str


def load_document(path: Path) -> Document:
    metadata = {}
    content_rst = StringIO()

    with path.open() as f:
        state = 0
        for line in f:
            if state == 0:
                if line.rstrip() == "---":
                    state = 1
                else:
                    break
            elif state == 1:
                if line.rstrip() == "---":
                    state = 2
                else:
                    key, value = map(str.strip, line.split(":", maxsplit=1))
                    metadata[key] = value
            else:
                content_rst.write(line)

    if state == 0:
        raise ValueError(
            f"Document {path.resolve()} doesn't start with a meta-data block"
        )
    elif state == 1:
        raise ValueError(
            f"Document {path.resolve()}'s meta-data block doesn't have an end"
        )

    return Document(metadata=metadata, content_rst=content_rst.getvalue())


@dataclass
class Page:
    title: str
    slug: str
    path: Optional[Path]
    content_rst: str


def load_page(path: Path) -> Page:
    document = load_document(path)
    try:
        title = document.metadata["title"]
    except KeyError:
        raise ValueError(f"Title not defined for page {path.resolve()}")

    try:
        slug = document.metadata["slug"]
    except KeyError:
        slug = slugify(title)

    return Page(title=title, slug=slug, path=path, content_rst=document.content_rst)


@dataclass
class Post(Page):
    date: DateTime
    modified: Optional[DateTime]


def load_post(path: Path) -> Post:
    document = load_document(path)
    try:
        title = document.metadata["title"]
    except KeyError:
        raise ValueError(f"Title not defined for post {path.resolve()}")

    try:
        slug = document.metadata["slug"]
    except KeyError:
        slug = slugify(title)

    try:
        date = document.metadata["date"]
    except KeyError:
        raise ValueError(f"Date not defined for post {path.resolve()}")
    else:
        date = DateTime.fromisoformat(date)

    try:
        modified = document.metadata["modified"]
    except KeyError:
        modified = None
    else:
        modified = DateTime.fromisoformat(modified)
        if modified < date:
            raise ValueError(
                f"Modification date is anterior to creation date for post {path.resolve()}"
            )

    return Post(
        title=title,
        slug=slug,
        path=path,
        date=date,
        modified=modified,
        content_rst=document.content_rst,
    )


def load_documents(
    path: Path, loader=load_document, glob: str = "*.rst"
) -> list[Document]:
    return list(map(loader, path.glob(glob)))


def load_pages(path: Path, glob="*.rst") -> list[Page]:
    return load_documents(path, loader=load_page, glob="**/*.rst")


def load_posts(path: Path) -> list[Path]:
    return load_documents(path, loader=load_post)


def render_template(tpl: Template, ctx: dict[str, Any], config: Config) -> str:
    ctx["SITE_NAME"] = config.site_name
    ctx["SITE_URL"] = config.site_url
    ctx["SITE_HOSTNAME"] = urlparse(config.site_url).hostname
    ctx["AUTHOR_NAME"] = config.author_name
    ctx["NOW"] = DateTime.now(tz=UTC)
    return tpl.render(ctx)


def render_page(page: Page, env: Environment, config: Config) -> str:
    return render_template(env.get_template("page.html"), {"page": page}, config)


def render_post(post: Post, env: Environment, config: Config) -> str:
    return render_template(env.get_template("post.html"), {"post": post}, config)


def render_index(posts: Iterable[Post], env: Environment, config: Config) -> str:
    return render_template(
        env.get_template("index.html"),
        {"posts": posts},
        config,
    )


def render_atom_feed(posts: Iterable[Post], env: Environment, config: Config) -> str:
    return render_template(
        env.get_template("atom.xml"),
        {"posts": posts},
        config,
    )


def main(args: Optional[Iterable[str]] = None):
    logging.basicConfig(level=logging.INFO)

    args_parser = ArgumentParser()
    args_parser.add_argument("--site-url", default="http://localhost:8000")
    args = args_parser.parse_args(args=args)

    logger.info("JSSG - Jtremesay's Static Site Generator")

    base_dir = Path()
    content_dir = base_dir / "content"
    pages_dir = content_dir / "pages"
    posts_dir = content_dir / "posts"
    static_dir = content_dir / "static"
    templates_dir = content_dir / "templates"
    output_dir = base_dir / "dist"

    config = Config(
        site_name="jtremesay.org",
        site_url=args.site_url,
        author_name="Jonathan Tremesaygues",
    )

    logger.info("paths:")
    logger.info("  base dir: %s", base_dir)
    logger.info("    content dir: %s", content_dir)
    logger.info("      pages dir: %s", pages_dir)
    logger.info("      posts dir: %s", posts_dir)
    logger.info("      static dir: %s", static_dir)
    logger.info("      templates dir: %s", templates_dir)
    logger.info("    output dir: %s", output_dir)

    logger.info("config:")
    logger.info("  site:")
    logger.info("    name: %s", config.site_name)
    logger.info("    url: %s", config.site_url)
    logger.info("  author:")
    logger.info("    name: %s", config.author_name)

    env = Environment(
        loader=FileSystemLoader(templates_dir), autoescape=select_autoescape()
    )
    env.filters["docutils"] = docutils_filter

    pages = load_pages(pages_dir)
    posts = sorted(load_posts(posts_dir), key=lambda e: e.date, reverse=True)

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("generating index")
    (output_dir / "index.html").write_text(render_index(posts, env, config))

    logger.info("generating posts")
    for post in posts:
        logger.info("  generating post %s.html from %s", post.slug, post.path)
        (output_dir / f"{post.slug}.html").write_text(render_post(post, env, config))

    logger.info("generating pages")
    output_pages_dir = output_dir / "pages"
    output_pages_dir.mkdir(parents=True, exist_ok=True)

    for page in pages:
        prefix = page.path.relative_to(pages_dir).parent
        page_output_dir = output_pages_dir / prefix
        page_output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            "  generating page %s/%s.html from %s", prefix, page.slug, page.path
        )
        (page_output_dir / f"{page.slug}.html").write_text(
            render_page(page, env, config)
        )

    logger.info("generating atom feed")
    (output_dir / f"atom.xml").write_text(render_atom_feed(posts, env, config))

    logger.info("copying static files")
    copy_tree(str(static_dir), str(output_dir / "static"))


if __name__ == "__main__":
    main()
