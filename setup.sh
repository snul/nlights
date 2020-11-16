if [ -f "user.data" ]; then
  rm user.data
fi

if [ -n "$(command -v yum)" ]; then
  sudo yum install python3 python3-pip pigpio screen
  sudo pip3 install pigpio requests
  sudo pigpiod
  python nlights.py
else
  if [ -n "$(command -v apt-get)" ]; then
    sudo apt-get -y install python3 python3-pip pigpio screen
    sudo pip3 install pigpio requests
    sudo pigpiod
    python nlights.py
  else
    echo "please install the packages python, python-pip, pigpio, screen"
  fi
fi
