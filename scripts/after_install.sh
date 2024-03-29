#!/bin/bash

cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
mv /home/ec2-user/ProjectFault/nginx.conf /etc/nginx/nginx.conf
cd /home/ec2-user/ProjectFault
source /home/ec2-user/projectFaultVenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
mv /home/ec2-user/ProjectFault/application/prod_config.py /home/ec2-user/ProjectFault/application/config.py
systemctl start nginx
/home/ec2-user/projectFaultVenv/bin/gunicorn app:app -b 127.0.0.1:8000 -D