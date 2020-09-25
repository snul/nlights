if [ -f "user.data" ]; then
	rm user.data
fi

if [ -n "$(command -v yum)" ]; then
	yum install python pigpio screen
	sudo pigpiod
	python nlights.py
else
	if [ -n "$(command -v apt-get)" ]; then
		sudo apt-get -y install python pigpio screen
		sudo pigpiod
		python nlights.py
	else
		echo "please install pigpio and screen"
	fi
fi