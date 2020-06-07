if [ -n "$(command -v yum)" ]; then
	yum install pigpio screen
	sudo lib/jdk1.8.0_221/bin/java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address=7777,suspend=n -Dfile.encoding=UTF-8 -jar nLights.jar createUser
else
	if [ -n "$(command -v apt-get)" ]; then
		sudo apt-get -y install pigpio screen
		sudo lib/jdk1.8.0_221/bin/java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address=7777,suspend=n -Dfile.encoding=UTF-8 -jar nLights.jar createUser
	else
		echo "please install pigpio and screen"
	fi
fi