from collections.abc import MutableSequence

from django.urls import URLPattern, path
from django.views.generic.base import RedirectView

from jssg import views
from jssg.models import Page, Post


def register_pages(urlpatterns: MutableSequence[URLPattern]):
    pages = Page.load_glob()
    urlpatterns.extend(
        path(
            f"pages/{page.slug}.html",
            views.PageView.as_view(slug=page.slug),
            name=f"page_{page.slug}",
        )
        for page in pages
    )


def register_posts(urlpatterns: MutableSequence[URLPattern]):
    posts = Post.load_glob()
    urlpatterns.extend(
        path(
            f"posts/{post.slug}.html",
            views.PostView.as_view(slug=post.slug),
            name=f"post_{post.slug}",
        )
        for post in posts
    )


urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="page_index"),
        name="index",
    ),
    path("atom.xml", views.PostFeedsView(), name="atom_feed"),
]
register_pages(urlpatterns)
register_posts(urlpatterns)
urlpatterns += [
    path("pages/<slug:slug>.html", views.PageView.as_view(), name="page"),
    path("posts/<slug:slug>.html", views.PostView.as_view(), name="post"),
]
