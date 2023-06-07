FROM node:lts AS frontend
WORKDIR /opt/jtremesay
COPY package.json package-lock.json ./
RUN npm install
COPY tsconfig.json vite.config.ts ./
COPY front front
RUN npm run build

FROM python AS yassg
RUN pip install build
WORKDIR /opt/jtremesay
COPY pyproject.toml MANIFEST.in ./
COPY yassg yassg
RUN python -m build --wheel

FROM python AS site
COPY --from=yassg /opt/jtremesay/dist/yassg-*.whl /tmp/
RUN pip install /tmp/yassg-*.whl
WORKDIR /opt/jtremesay
COPY Makefile ./
COPY theme theme
COPY static static
COPY content content
COPY --from=frontend /opt/jtremesay/out/static/gen out/static/gen
RUN make

FROM nginx AS serve
COPY --from=site /opt/jtremesay/out /usr/share/nginx/html