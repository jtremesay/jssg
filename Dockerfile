FROM python AS yassg
RUN pip install build
WORKDIR /opt/jtremesay
COPY pyproject.toml MANIFEST.in ./
COPY yassg yassg
RUN python -m build --wheel

FROM python AS site
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs
WORKDIR /opt/jtremesay
COPY package.json package-lock.json ./
RUN npm install
COPY --from=yassg /opt/jtremesay/dist/yassg-*.whl /tmp/
RUN pip install /tmp/yassg-*.whl
WORKDIR /opt/jtremesay
COPY Makefile tsconfig.json vite.config.ts ./
COPY theme theme
COPY static static
COPY front front
COPY content content
RUN make

FROM nginx AS serve
COPY --from=site /opt/jtremesay/out /usr/share/nginx/html