import os
import time
import random
import schedule
from loguru import logger
from locationsharinglib import Service
from paho.mqtt import client as mqtt_client
from cookieshandler import CookiesHandler



cookies_file = "./cookies" + os.get_env("COOKIES_FILE_NAME")
google_email = os.get_env("EMAIL_ADDRESS")
update_interval = os.get_env("UPDATE_INTERVAL")
cookieshandler = CookiesHandler()


service = Service(cookies_file=cookies_file, authenticating_account=google_email)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.error("Failed to connect, return code %d\n" +  rc)

    client = mqtt_client.Client(f'python-mqtt-{random.randint(0, 1000)}')
    client.username_pw_set(os.get_env("MQTT_USERNAME"), os.get_env("MQTT_PASSWORD"))
    client.on_connect = on_connect
    client.connect(os.get_env("MQTT_HOST"), os.get_env("MQTT_PORT"))
    return client

def publish(client):
    for person in service.get_all_people():
        id = str(getattr(person, "nickname"))
        if "@" in id:
            id = id.split("@")[0]
        tracker_id = '{"state_topic": "' +  id +'/state", "name": "' +  id +'", "payload_home": "home", "payload_not_home": "not_home", "json_attributes_topic": "' +  id +'/attributes"}'
        client.publish('homeassistant/device_tracker/' +  id +'/config',tracker_id)
        attrubutes = '{"latitude": '+str(getattr(person, "latitude"))+', "longitude": '+str(getattr(person, "longitude"))+', "gps_accuracy": '+str(getattr(person, "accuracy"))+', "battery_level": '+str(getattr(person, "battery_level"))+'}'
        client.publish( id + '/attributes',attrubutes)

def run():
    publish(client)


if __name__ == "__main__":
    client = connect_mqtt()
    client.loop_start()
    schedule.every(30).minutes.do(cookieshandler.refresh)
    schedule.every(update_interval).minutes.do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)
