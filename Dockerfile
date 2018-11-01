FROM python:3-alpine

RUN apk add --update python3-dev build-base linux-headers pcre-dev uwsgi-python3 nodejs npm git

RUN npm install -g bower

RUN npm install -g grunt

WORKDIR /opt/

RUN git clone https://github.com/ProjectMirador/mirador.git

WORKDIR /opt/mirador

RUN npm install

RUN bower --allow-root install

RUN grunt

RUN mkdir /opt/mirador-proxy/

RUN mkdir /opt/mirador-proxy/cache/

RUN cp -r ./build/ /opt/mirador-proxy/

RUN pip3 install --upgrade pip

RUN pip3 install uwsgi

COPY *.py /opt/mirador-proxy/

COPY *.html /opt/mirador-proxy/

COPY *.txt /opt/mirador-proxy/

WORKDIR /opt/mirador-proxy/

RUN pip3 install -r requirements.txt

# Expose port 8000 for uwsgi

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", \
            "--uid", "uwsgi", \
               "--protocol", "uwsgi", \
               "--enable-threads", \
               "--master", \
               "--http-timeout", "600", \
               "--module", "mirador:app", "--processes", "1", "--threads", "8"]