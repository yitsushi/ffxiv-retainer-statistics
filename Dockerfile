FROM python:3.7-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dist /dist
RUN pip install --no-cache-dir dist/ffxivstat-*.whl

VOLUME ["/data"]
EXPOSE 80
