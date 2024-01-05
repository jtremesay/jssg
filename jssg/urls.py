from django.urls import path
from django.views.generic.base import RedirectView

from jssg import views

urlpatterns = [
    path("", RedirectView.as_view(url="/pages/index.html"), name="index"),
    path("atom.xml", views.PostFeedsView(), name="atom_feed"),
    path("pages/<slug:slug>.html", views.PageView.as_view(), name="page"),
    path("posts/<slug:slug>.html", views.PostView.as_view(), name="post"),
]
