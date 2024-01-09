# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2023 Jonathan Tremesaygues
#
# Dockerfile
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
FROM python:3.12 AS site

# Update packages and install needed stuff
RUN pip install -U pip setuptools wheel

# Install python & node deps
WORKDIR /code
COPY requirements.txt ./
RUN pip install -Ur requirements.txt

# Copy source dir
COPY manage.py ./
COPY jssg/ jssg/
COPY content/ content/

# Build
RUN ./manage.py distill-local --collectstatic --force dist

FROM nginx:mainline
COPY --from=site /code/dist/ /usr/share/nginx/html/
