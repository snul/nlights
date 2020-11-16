#!/bin/bash
if [ -d .git ]; then
  echo 'check internet connection'
  x='0'
  while [ $x == '0' ]; do
    ping -c1 -w5 www.google.com >/dev/null 2>&1
    if [ $? -eq 0 ]; then
      echo 'connected'
      x=1
    else
      echo 'waiting for connection'
      sleep 1
    fi
  done
  sudo git init
  sudo git reset --hard origin/master
  sudo git pull origin master
else
  echo 'git not installed, please install git for updates.'
fi

sudo python3 -m pip install pigpio requests
sudo pigpiod
sudo screen -amdS nLights sudo python3 nlights.py
echo 'nLights successfully started as new screen session in the background.'
