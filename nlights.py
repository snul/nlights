import os
import sys
import json
import time
import traceback
from datetime import datetime


try:
    import requests
    import pigpio
    from requests.exceptions import ConnectionError, Timeout
except ImportError:
    print("Trying to Install required modules.")
    os.system('python -m pip install requests pigpio')
    time.sleep(2)
    import requests
    import pigpio
    from requests.exceptions import ConnectionError, Timeout


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

# message ids for json requests
MSG_ID_LOAD_VALUES = 2
MSG_ID_CHECK_IF_USERNAME_EXISTS = 3

SERVER_ERROR_MESSAGE = "Server seems to be unresponsive at the moment, please try again later or contact us: " \
                       "support@nlights.at"


def start():
    error_counter = 0
    init()

    while True:
        try:
            time.sleep(0.5)
            update_values()
            if error_counter != 0:
                if error_counter > 15:
                    log("Reconnected.")
                error_counter = 0
        except KeyboardInterrupt:
            sys.exit()
        except (ServerError, InvalidResponseError) as e:
            # do not log occasional connection errors
            error_counter += 1
            if error_counter > 15:
                # more than 15 sec disconnected
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
    try:
        data = {'id': MSG_ID_CHECK_IF_USERNAME_EXISTS, 'username': username}
        response = requests.post(url, data=json.dumps(data),
                                 headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        if response.status_code != 200:
            raise ServerError(SERVER_ERROR_MESSAGE)
        else:
            json_response = response.json()
            if json_response['status'] == 1:
                return True
            else:
                return False
    except ConnectionError:
        raise ServerError(SERVER_ERROR_MESSAGE)
    except ValueError:
        # response.json() failed
        raise ServerError(SERVER_ERROR_MESSAGE)


# loads the values from the database and sets them to the led strip
def update_values():
    try:
        data = {'id': MSG_ID_LOAD_VALUES, 'username': username}
        response = requests.post(url, data=json.dumps(data),
                                 headers={'Content-type': 'application/json', 'Accept': 'text/plain'}, timeout=1)
        if response.status_code != 200:
            raise ServerError(SERVER_ERROR_MESSAGE)
        else:
            json_response = response.json()
            if json_response['status'] == 1:
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
    except (ConnectionError, Timeout):
        raise ServerError(SERVER_ERROR_MESSAGE)
    except ValueError:
        # response.json() failed
        raise ServerError(SERVER_ERROR_MESSAGE)


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
