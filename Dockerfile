FROM node:lts AS front
WORKDIR /opt/jtremesay
COPY package.json package-lock.json ./
RUN npm install
COPY Makefile tsconfig.json vite.config.ts ./
COPY front front
RUN make front


FROM python AS site
RUN pip install -U pip setuptools wheel
WORKDIR /opt/jtremesay
COPY requirements.txt ./
RUN pip install -Ur requirements.txt
COPY pelicanconf.py publishconf.py Makefile ./
COPY theme theme
COPY fragments fragments
RUN make fragments
COPY content content
COPY --from=front /opt/jtremesay/content/static/gen ./content/static/gen 
RUN make publish


FROM nginx AS serve
COPY --from=site /opt/jtremesay/output /usr/share/nginx/html