#!/bin/bash
if [ -d .git ]; then
 echo 'check internet connection'
 x='0'
 y='0'
 z='15'
 while [ $x == '0' ]
 do
   ping -c1 -w5 www.google.com > /dev/null 2>&1
   if [ $? -eq 0 ]; then
     echo 'connected'
     x=1
   else
    echo 'waiting for connection'
    sleep 1
    y=$((y+1))
    if [ "$y" -gt "$z" ]; then
    file='./userdata/settings.properties'
    backupfile='./userdata/backup_settings.properties'

     if [ -e "$file" ]; then
      PROP_KEY='offlineMode'
      PROP_VALUE=`cat $file | grep "$PROP_KEY" | cut -d'=' -f2`
      if [ "$PROP_VALUE" == 'true' ]; then
       echo 'no internet connection'
       echo 'starting in offline Mode with stored values. Please restart as soon as internet connection is active.'
       x=1
      fi
     else
      echo 'offlineMode not set.'
     fi

     if [ -e "$backupfile" ]; then
       PROP_KEY='offlineMode'
       PROP_VALUE=`cat $backupfile | grep "$PROP_KEY" | cut -d'=' -f2`
       if [ "$PROP_VALUE" == 'true' ]; then
        echo 'no internet connection'
        echo 'starting in offline Mode with stored values from backup file. Please restart as soon as internet connection is active.'
        x=1
       fi
      else
       echo 'offlineMode not set.'
      fi
     fi
    fi
 done
 sudo git init
 sudo git reset --hard origin/master
 sudo git pull origin master
else
  echo 'git not installed, please install git for updates.'
fi;

[[ ! -x lib/jdk1.8.0_221/bin/java ]] && echo "Check executable permissions for 'lib/jdk1.8.0_221/bin/java'."

sudo killall pigpiod || true && sudo pigpiod && sudo screen -amdS nLights sudo lib/jdk1.8.0_221/bin/java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,address=7777,suspend=n -Dfile.encoding=UTF-8 -jar nLights.jar && echo 'nLights sucessful started as new screen session in the background.'
