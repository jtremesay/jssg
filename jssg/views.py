from typing import Any, Optional

from django.contrib.syndication.views import Feed
from django.http import HttpRequest
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.views.generic.base import TemplateView

from jssg.models import Page, Post


class PostFeedsView(Feed):
    title = "jtremesay - derniers articles"
    link = ""
    feed_type = Atom1Feed

    def items(self) -> list[Post]:
        return sorted(Post.load_glob(), key=lambda p: p.timestamp, reverse=True)[:20]

    def item_title(self, post: Post) -> str:
        return post.title

    def item_description(self, item: Post):
        return item.content_md

    def item_link(self, post: Post) -> str:
        return reverse("post", args=(post.slug,))

    def item_pubdate(self, post: Post) -> str:
        return post.timestamp


class PageView(TemplateView):
    template_name = "jssg/page.html"
    page_cls = Page
    slug: Optional[str] = None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        try:
            self.slug = kwargs["slug"]
        except:
            ...
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = self.page_cls.load_page_with_slug(self.slug)
        return ctx


class PostView(PageView):
    template_name = "jssg/post.html"
    page_cls = Post
