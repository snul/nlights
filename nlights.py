import os
import sys
import json
import time
import traceback
from datetime import datetime


try:
    import requests
    import pigpio
    from requests.exceptions import ConnectionError
except ImportError:
    print("Trying to Install required modules.")
    os.system('python -m pip install requests pigpio')
    time.sleep(2)
    import requests
    import pigpio
    from requests.exceptions import ConnectionError


class Error(Exception):
    # base class for custom exceptions
    pass


class ServerError(Error):
    # invalid response status code
    pass


class InvalidResponseError(Error):
    # correct status code but invalid response or not found
    pass


url = "http://api.nlights.at/"
filename = "user.data"
pi = pigpio.pi()
username = ""
activatedSet = set()


def start():
    error_counter = 0
    init()

    while True:
        try:
            time.sleep(0.5)
            update_values()
            if error_counter != 0:
                log("Reconnected.")
                error_counter = 0
        except KeyboardInterrupt:
            sys.exit()
        except (ServerError, InvalidResponseError) as e:
            # do not log occasional connection errors
            error_counter += 1
            if error_counter > 5:
                log(e.message)
        except:
            traceback.print_exc()


# reads the username from the file or starts the setup
def init():
    # read username from file
    if os.path.isfile(filename):
        f = open(filename, "r")
        global username
        username = f.read()
        f.close()
        # check if username is valid
        if username_exists():
            log("nLights started successfully")
        else:
            setup()
    else:
        setup()


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
            print('Username does not exist, please try again or create a new one with the nLights App from the '
                  'AppStore or PlayStore.')

    f = open(filename, "w")
    f.write(username)
    f.close()

    print("")
    log("nLights started successfully")
    print("Restart the application using the start.sh script to automatically start nLights in the background.")


# checks if a username exists and is valid
def username_exists():
    data = {'id': 3, 'username': username}
    response = requests.post(url, data=json.dumps(data),
                             headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    if response.status_code != 200:
        log('Server error, please try again later.')
        return False
    else:
        json_response = response.json()
        if json_response['status'] == 0:
            return True
        else:
            return False


# loads the values from the database and sets them to the led strip
def update_values():
    try:
        data = {'id': 12, 'username': username}
        response = requests.post(url, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        if response.status_code != 200:
            raise ServerError("Server seems to be unresponsive at the moment.")
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
                raise InvalidResponseError("Invalid server response status code.")
    except ConnectionError:
        raise ServerError("Server seems to be unresponsive at the moment.")


# sets the given rgb values to the given rgb pins
def set_rgb(pin_red, pin_green, pin_blue, value_red, value_green, value_blue):
    pi.set_PWM_dutycycle(pin_red, value_red)
    pi.set_PWM_dutycycle(pin_green, value_green)
    pi.set_PWM_dutycycle(pin_blue, value_blue)


def log(message):
    dt = datetime.utcnow()
    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp + " (UTC): " + message)


start()
