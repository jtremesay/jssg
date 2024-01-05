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
from django.urls import path
from django.views.generic.base import RedirectView

from jssg import views

urlpatterns = [
    path("", RedirectView.as_view(url="/pages/index.html"), name="index"),
    path("atom.xml", views.PostFeedsView(), name="atom_feed"),
    path("pages/<slug:slug>.html", views.PageView.as_view(), name="page"),
    path("posts/<slug:slug>.html", views.PostView.as_view(), name="post"),
]
