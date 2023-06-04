FROM node:lts AS js
WORKDIR /opt/jtremesay
COPY package.json package-lock.json ./
RUN npm install
COPY tsconfig.json vite.config.ts ./
COPY src src
RUN npm run build

FROM python AS base
RUN pip install build
WORKDIR /opt/jtremesay
COPY pyproject.toml MANIFEST.in ./
COPY jtremesay jtremesay
COPY --from=js /opt/jtremesay/jtremesay/static/gen jtremesay/static/gen
RUN python -m build --wheel


FROM python AS prod
COPY --from=base /opt/jtremesay/dist/jtremesay-*.whl /tmp/
RUN pip install /tmp/jtremesay-*.whl
RUN rm /tmp/*.whl
EXPOSE 8003
CMD python -m hypercorn 'jtremesay:create_app()' --bind '0.0.0.0:8003' --worker-class uvloop
