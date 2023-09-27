#!/bin/bash

PORT=8000
PID=$(lsof -t -i :$PORT)
kill $PID
systemctl stop nginx
rm -rf /home/ec2-user/ProjectFault