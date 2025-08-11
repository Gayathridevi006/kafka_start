import requests 
import json
import logging
import time
from quixstreams import Application
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

def data_get():
    app = Application(broker_address="localhost:9092",
                    loglevel="DEBUG",
                    consumer_group="weather_reader")
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
                key = msg.key().decode('utf-8')
                value = json.load(msg.value())
                offset = msg.offset()
                timestamp = msg.timestamp()
                print(f"Received message with key: {key}, value: {value}, offset: {offset}, timestamp: {timestamp}")


# print(str(producer))

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()

