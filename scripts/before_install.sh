#!/bin/bash

pkill -f "gunicorn app:app"
systemctl stop nginx
rm -rf /home/ec2-user/ProjectFault