#!/bin/bash

cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
mv /home/ec2-user/ProjectFault/nginx.conf /etc/nginx/nginx.conf
cd /home/ec2-user/ProjectFault
source /home/ec2-user/projectFaultVenv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
mv /home/ec2-user/ProjectFault/application/prod_config.py /home/ec2-user/ProjectFault/application/config.py
bash /home/ec2-user/ProjectFault/scripts/start_server.sh &