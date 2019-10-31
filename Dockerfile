FROM python:3.7-alpine

RUN apk add --no-cache postgresql-libs && \
      apk add --no-cache --virtual \
            .build-deps gcc musl-dev openssl-dev \
            libffi-dev postgresql-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dist /dist
RUN pip install --no-cache-dir dist/ffxivstat-*.whl

RUN apk --purge del .build-deps

VOLUME ["/data"]
EXPOSE 80
