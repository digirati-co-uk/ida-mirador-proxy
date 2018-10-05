FROM centos

RUN yum -y update

RUN yum -y install epel-release

RUN yum -y install gcc

RUN yum -y install python-pip

RUN yum -y install python-devel

RUN yum -y install nodejs 

RUN yum -y install npm 

RUN yum -y install git

RUN yum -y install bzip2

RUN npm install -g bower 

RUN npm install -g grunt

WORKDIR /opt/

RUN git clone https://github.com/ProjectMirador/mirador.git

WORKDIR /opt/mirador

RUN npm install

RUN bower --allow-root install

RUN grunt


RUN mkdir /opt/mirador-proxy/

RUN cp -r ./build/ /opt/mirador-proxy/
RUN cp -r ./locales/ /opt/mirador-proxy/
RUN cp -r ./images/ /opt/mirador-proxy/
RUN cp -r . /opt/mirador-proxy/

RUN pip install --upgrade pip

RUN pip install uwsgi


COPY *.py /opt/mirador-proxy/

COPY *.html /opt/mirador-proxy/

COPY *.sh /opt/mirador-proxy/

COPY *.txt /opt/mirador-proxy/

WORKDIR /opt/mirador-proxy/

RUN pip install -r requirements.txt


# CMD ./run_mirador.sh

# Expose port 8000 for uwsgi

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "mirador:app", "--processes", "1", "--threads", "8"]