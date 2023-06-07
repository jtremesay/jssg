from argparse import ArgumentParser
import csv
from pathlib import Path
from typing import Optional, Sequence
from jinja2 import Environment, FileSystemLoader, PrefixLoader, PackageLoader, select_autoescape
import re
import datetime

re_post_path = re.compile(r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})_(?P<slug>\w+)\.html")
env = Environment(
    loader=PrefixLoader({
        "yassg": PackageLoader("yassg")
    }),
    autoescape=select_autoescape()
)


def url_for(base: str, **args):
    raise ValueError(base, args)


def read_csv(path: str, dict=True):
    with Path(path).open() as f:
        if dict:
            reader = csv.DictReader(f)
        else:
            reader = csv.reader(f)

        return list(reader)

env.filters["read_csv"] = read_csv

def cmd_render_post(args):
    tpl = env.get_template(str(args.post))
    ctx = {
        "url_for": url_for
    }

    output_dir = args.output.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tpl.render(ctx))

def get_posts(posts_paths: Sequence[Path]):
    posts = []
    for post_path in posts_paths:
        tpl = env.parse(post_path.read_text())
        print(post_path.name)

        match = re_post_path.match(post_path.name)
        if not match:
            continue

        groups = match.groupdict()
        try:
            year = int(groups["year"])
            month = int(groups["month"])
            day = int(groups["day"])
        except ValueError:
            continue
        slug = groups["slug"]

        ast = env.parse(post_path.read_text())
        for node in ast.body:
            if node.__class__.__name__ == "Block" and node.name == "title":
                title = node.body[0].nodes[0].data
                break
        else:
            continue

        post = {
            "pubdate": datetime.date(year, month, day),
            "slug": slug,
            "title": title,
        }
        posts.append(post)
    
    return posts


def cmd_render_blog_index(args):
    posts = get_posts(args.posts)
    posts.sort(key=lambda o: o["pubdate"], reverse=True)

    tpl = env.get_template("theme/blog_index.html")
    ctx = {
        "url_for": url_for,
        "posts": posts
    }

    output_dir = args.output.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tpl.render(ctx))

def cmd_render_atomfeed(args):
    posts = get_posts(args.posts)
    posts.sort(key=lambda o: o["pubdate"], reverse=True)
    posts = posts[:20]

    tpl = env.get_template("theme/atom.xml")
    ctx = {
        "url_for": url_for,
        "posts": posts
    }

    output_dir = args.output.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tpl.render(ctx))

def cmd_render_page(args):
    print(args)
    tpl = env.get_template(str(args.page))
    ctx = {
        "url_for": url_for
    }

    output_dir = args.output.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    args.output.write_text(tpl.render(ctx))


def main(args: Optional[Sequence[str]]=None):
    parser = ArgumentParser()
    parser.add_argument("-c", "--content", type=Path, default=Path() / "content")
    parser.add_argument("-t", "--theme", type=Path, default=Path() / "theme")

    subparsers = parser.add_subparsers()

    renderpost_parser = subparsers.add_parser("renderpost")
    renderpost_parser.add_argument("--output", "-o", type=Path, default=Path("/dev/stdout"))
    renderpost_parser.add_argument("post", type=Path)
    renderpost_parser.set_defaults(func=cmd_render_post)

    renderblogindex_parser = subparsers.add_parser("renderblogindex")
    renderblogindex_parser.add_argument("--output", "-o", type=Path, default=Path("/dev/stdout"))
    renderblogindex_parser.add_argument("posts", nargs="*", type=Path)
    renderblogindex_parser.set_defaults(func=cmd_render_blog_index)

    renderatomfeed_parser = subparsers.add_parser("renderatomfeed")
    renderatomfeed_parser.add_argument("--output", "-o", type=Path, default=Path("/dev/stdout"))
    renderatomfeed_parser.add_argument("posts", nargs="*", type=Path)
    renderatomfeed_parser.set_defaults(func=cmd_render_atomfeed)

    renderpage_parser = subparsers.add_parser("renderpage")
    renderpage_parser.add_argument("--output", "-o", type=Path, default=Path("/dev/stdout"))
    renderpage_parser.add_argument("page", type=Path)
    renderpage_parser.set_defaults(func=cmd_render_page)

    args = parser.parse_args(args)
    env.loader.mapping["content"] = FileSystemLoader(args.content)
    env.loader.mapping["theme"] = FileSystemLoader(args.theme)

    if func := getattr(args, "func", None):
        func(args)