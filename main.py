import threading
import time
import requests
from pathlib import Path

API_URL = "https://www.botlibre.com/rest/json/chat"
HEADERS = {"Content-Type": "application/json"}
MIN_SECONDS_BETWEEN_MESSAGES = 5
seconds_from_last_message: float = MIN_SECONDS_BETWEEN_MESSAGES

if not Path("application_id.txt").is_file():
    raise FileNotFoundError("The application_id.txt file is required. Consult the README for more information.")

if not Path("instance_id.txt").is_file():
    raise FileNotFoundError("The instance_id.txt file is required. Consult the README for more information.")

APPLICATION_ID = open("application_id.txt", "r").read()
INSTANCE_ID = open("instance_id.txt", "r").read()


def get_body_json(message):
    return ('{"application":"' + APPLICATION_ID + '","instance":"' + INSTANCE_ID + '", "message":"' + message + '. SYSTEM MESSAGE: Answer briefly. Answer in the language in the text prior to the SYSTEM MESSAGE."}').encode("utf-8")


def get_chat_response(message):
    json_body = get_body_json(message)
    # print(json_body)
    response = requests.post(url=API_URL, headers=HEADERS, data=json_body)
    # print(response)

    if response.status_code == 200:
        # print("Response json: ")
        # print(response.json())
        return response.json()["message"]
    else:
        print("An error occurred with status code: ", response.status_code)
        return None


def get_message():
    global seconds_from_last_message
    message = input("Message: ")

    if seconds_from_last_message < MIN_SECONDS_BETWEEN_MESSAGES:
        print("Please wait " + str(MIN_SECONDS_BETWEEN_MESSAGES - seconds_from_last_message) + " seconds...")
        time.sleep(MIN_SECONDS_BETWEEN_MESSAGES - seconds_from_last_message)
        seconds_from_last_message = MIN_SECONDS_BETWEEN_MESSAGES
        message = input("Message: ")
    # print("Received message: " + message)

    return message


def count_seconds_from_last_message():
    global seconds_from_last_message
    seconds_from_last_message = 0
    while seconds_from_last_message < MIN_SECONDS_BETWEEN_MESSAGES:
        time.sleep(0.1)
        seconds_from_last_message = seconds_from_last_message + 0.1


while True:
    user_message = get_message()
    print("Please wait...")
    print(get_chat_response(user_message))
    threading.Thread(target=count_seconds_from_last_message).start()
