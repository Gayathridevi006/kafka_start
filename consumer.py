import requests 
import json
import logging
import time
from quixstreams import Application
from datetime import datetime
response = requests.get("https://api.open-meteo.com/v1/forecast", 
                        params={ "latitude":51.5 ,
                                 "longitude": -0.11, 
                                 "current": "temperature_2m"})
weather = response.json()

def main():
    app = Application(broker_address="localhost:9092",
                    loglevel="DEBUG"
    )
    with app.get_producer() as producer:
        producer.produce(topic = "weather_data_demo",
                        key="london",
                        value=json.dumps(weather),
                        )
        print("Message sent successfully")
        producer.flush()
        logging.info("Produced... Sleepinggg")
        time.sleep(2)

def get_date(msg):
    if msg:
        t_type, t_ms = msg.timestamp()
        dt = datetime.fromtimestamp(t_ms / 1000)  # divide by 1000 to get seconds
        print(dt)  # local time
        print(dt.isoformat())
    return dt

def data_get():
    app = Application(broker_address="localhost:9092",
                    loglevel="DEBUG",
                    consumer_group="weather_reader"
                    , auto_offset_reset="earliest")
    #auto_offset_reset="earliest" --> will start offset 0 and gets entire history
    #auto_offset_reset="latest" --> will start from latest offset and gets only new messages and ignore old messages
    with app.get_consumer() as consumer:
        consumer.subscribe(["weather_data_demo"])
        while True:
            msg = consumer.poll(1)
            print(msg)
            if msg is None:
                print("waiting for new data msg")
            elif msg.error():
                logging.error(f"Error: {msg.error()}")
            else:
                key = msg.key().decode("utf-8")
                value = json.loads(msg.value())
                offset = msg.offset()
                timestamp = get_date(msg=msg)
                print(f"Received message with key: {key}, value: {value}, offset: {offset}, timestamp: {timestamp}")
                consumer.store_offsets(msg)


# print(str(producer))

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    try:
        data_get()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

