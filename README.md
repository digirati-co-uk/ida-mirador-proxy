# ida-mirador-proxy
Lightweight flask app to serve manifests via Mirador.

## Build Notes (to turn into Dockerfile)

```bash

sudo yum -y update

sudo yum -y install epel-release

sudo yum -y install nodejs npm git

sudo npm install -g bower

sudo npm install -g grunt
 
git clone https://github.com/ProjectMirador/mirador.git

cd mirador

npm install

bower install

grunt

mkdir /opt/mirador-proxy

cp -r ./mirador/ /opt/mirador-proxy/


[Vagrant] sudo fallocate -l 8G /swapfile 


```
