#!/bin/bash
/home/ec2-user/projectFaultVenv/bin/gunicorn app:app -b 127.0.0.1:8000