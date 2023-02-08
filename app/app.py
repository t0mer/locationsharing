import os
import time
import random
import json
import schedule
import re
from loguru import logger
from locationsharinglib import Service
from paho.mqtt import client as mqtt_client
from cookieshandler import CookiesHandler



cookies_file = "./cookies/" + os.getenv("COOKIES_FILE_NAME")
google_email = os.getenv("EMAIL_ADDRESS")
update_interval = os.getenv("UPDATE_INTERVAL")
cookieshandler = CookiesHandler()


service = Service(cookies_file=cookies_file, authenticating_account=google_email)

def convert_word(word):
    english = {"א": "a", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "v", "ז": "z", "ח": "h", "ט": "t", "י": "y",
               "כ": "c", "ך": "c", "ל": "l", "מ": "m", "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "a", "פ": "p",
               "ף": "p", "צ": "ch", "ץ": "ch", "ק": "k", "ר": "r", "ש": "sh", "ת": "t", }
    result = ""
    word = re.sub('\W+', '', word)
    if word.encode().isalpha():
        return word
    elif re.search('[a-zA-Z]', word):
        return ''.join(list(filter(lambda ele: re.search("[a-zA-Z\s]+", ele) is not None, word)))
    else:
        try:
            for char in word:
                result = result + english[char]
            return result
        except Exception as e:
            print(e)
            
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error("Failed to connect, return code %d\n" +  rc)

    client = mqtt_client.Client(f'python-mqtt-{random.randint(0, 1000)}')
    client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
    client.on_connect = on_connect
    client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))
    return client

def publish(client):
    persons = service.get_all_people()
    # logger.info("Number of peoples: " + str(len(persons)))
    for person in persons:
        id = convert_word(str(getattr(person, "nickname")))
        logger.info("Person: " + id)
        if "@" in id:
            id = id.split("@")[0]
        id = id.replace(".","_")
        tracker_id = '{"state_topic": "' +  id +'/state", "name": "' +  id +'", "payload_home": "home", "payload_not_home": "not_home", "json_attributes_topic": "' +  id +'/attributes"}'
        client.publish('homeassistant/device_tracker/' +  id +'/config',tracker_id)
        attrubutes = {"latitude": getattr(person, "latitude"), "longitude": getattr(person, "longitude"), "gps_accuracy": getattr(person, "accuracy"), "battery_level": getattr(person, "battery_level")}
        client.publish( id + '/attributes',json.dumps(attrubutes))

def run():
    publish(client)


if __name__ == "__main__":
    client = connect_mqtt()
    client.loop_start()
    schedule.every(30).minutes.do(cookieshandler.refresh)
    schedule.every(int(update_interval)).minutes.do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)
