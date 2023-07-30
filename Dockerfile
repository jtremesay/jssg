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