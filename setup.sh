if [ -f "user.data" ]; then
  rm user.data
fi

if [ -n "$(command -v yum)" ]; then
  sudo yum install python3 python3-pip pigpio screen
  python3 -m pip install pigpio requests
  sudo pigpiod
  python3 nlights.py
else
  if [ -n "$(command -v apt-get)" ]; then
    sudo apt-get -y install python3 python3-pip pigpio screen
    python3 -m pip install pigpio requests
    sudo pigpiod
    python3 nlights.py
  else
    echo "please install the packages python3, python3-pip, pigpio, screen"
  fi
fi
