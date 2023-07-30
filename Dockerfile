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

FROM node as front
WORKDIR /code
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY tsconfig.json vite.config.ts ./
COPY front/ front/
RUN npm run build

FROM python AS site
WORKDIR /code
COPY requirements.txt ./
RUN pip install -U pip setuptools wheel && pip install -Ur requirements.txt
COPY jssg.py ./
COPY content/ content/
COPY --from=front /code/content/static/gen/ content/static/gen/
RUN python jssg.py --site-url https://jtremesay.org

FROM nginx
COPY --from=site /code/dist/ /usr/share/nginx/html/
EXPOSE 8000