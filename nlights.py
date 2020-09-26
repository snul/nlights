import os
import sys
import json
import time
import traceback

try:
	import requests
	import pigpio
except ImportError:
	print "Trying to Install required modules.\n"
	os.system('python -m pip install requests pigpio')
	time.sleep(2)
	import requests
	import pigpio


url = "http://api.nlights.at/"
filename = "user.data"
pi = pigpio.pi()
username = ""
activatedSet = set()


def start():
	# read username from file
	if os.path.isfile(filename):
		f = open(filename, "r")
		global username
		username = f.read()
		f.close()
		# check if username is valid
		if username_exists():
			print("nLights started successfully")
		else:
			setup()
	else:
		setup()

	while True:
		try:
			update_values()
			time.sleep(0.5)
		except KeyboardInterrupt:
			sys.exit()
		except:
			traceback.print_exc()


# launches the setup to enter the username
def setup():
	print("")
	print("Hello!")
	print("Please enter your username.")
	print("To create a user, download the nLights App from the AppStore or PlayStore and create a new account.")

	global username

	# check if username exists
	while not username_exists():
		username = raw_input("Username: ")
		if not username_exists():
			print('Username does not exist, please try again or create a new one with the nLights App from the AppStore or PlayStore.')

	f = open(filename, "w")
	f.write(username)
	f.close()

	print("")
	print("nLights started successfully")
	print("Restart the application using the start.sh script to automatically start nLights in the background.")


# checks if a username exists and is valid
def username_exists():
	data = {'id': 3, 'username': username}
	response = requests.post(url, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
	if response.status_code != 200:
		print('Server error, please try again later.')
		return False
	else:
		json_response = response.json()
		if json_response['status'] == 0:
			return True
		else:
			return False


# loads the values from the database and sets them to the led strip
def update_values():
	data = {'id' : 2, 'username': username}
	response = requests.post(url, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
	if response.status_code != 200:
		print('Server error, please try again later.')
	else:
		json_response = response.json()
		if json_response['status'] == 0:
			for rgbRow in json_response['values']:
				pin_red = rgbRow['pinRed']
				pin_green = rgbRow['pinGreen']
				pin_blue = rgbRow['pinBlue']
				value_red = rgbRow['red']
				value_green = rgbRow['green']
				value_blue = rgbRow['blue']

				# check if they were enabled and set values to 0 in case they were disabled
				if rgbRow['status'] == 0:
					if rgbRow['id'] in activatedSet:
						set_rgb(pin_red, pin_green, pin_blue, 0, 0, 0)
						activatedSet.discard(rgbRow['id'])
				else:
					activatedSet.add(rgbRow['id'])
					set_rgb(pin_red, pin_green, pin_blue, value_red, value_green, value_blue)
		else:
			print('Failed to load data.')


# sets the given rgb values to the given rgb pins
def set_rgb(pin_red, pin_green, pin_blue, value_red, value_green, value_blue):
	pi.set_PWM_dutycycle(pin_red, value_red)
	pi.set_PWM_dutycycle(pin_green, value_green)
	pi.set_PWM_dutycycle(pin_blue, value_blue)


start()