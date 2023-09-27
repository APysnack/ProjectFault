#!/bin/bash -e

PORT=8000
PID=$(sudo lsof -t -i :$PORT)

if [ -z "$PID" ]; then
  echo "No process found using port $PORT."
else
  sudo kill $PID
  echo "Killed process with PID $PID using port $PORT."
fi
