import logging
from quixstreams import Application 

def main():
    logging.info("START")
    app = Application(broker_address="localhost:9092",
                      loglevel="DEBUG",
                      auto_offset_reset="earliest",
                      consumer_group="weather_processor") ## identify which application with unique string
    input_topic = app.topic("weather_data_demo")
    output_topic = app.topic("weather_data_demo_output")

    streaming_df = app.dataframe(input_topic)
    # Example transformation: Add a new column with a constant value
    streaming_df = streaming_df.apply(transform)
    streaming_df = streaming_df.to_topic(output_topic)

    app.run(streaming_df)
def transform(msg):
    """
    Example transformation function that adds a new column to the DataFrame.
    """
    celcius = msg["current"]["temperature_2m"]
    farenheit = (celcius * 9/5 )+ 32
    kelvin = celcius + 273.15
    logging.debug("Transforming message: %s", msg)
    logging.debug("Temperature in Celsius: %s", celcius)
    logging.debug("Temperature in Kelvin: %s", kelvin)
    logging.debug("Temperature in Fahrenheit: %s", farenheit)
    new_msg =  {
            "temperature_in_celcius": celcius,
            "temperature_in_farenheit": round(farenheit,2),
            "temperature_in_kelvin": round(kelvin, 2)
        }
    logging.debug("Returning : %s", new_msg)
    return new_msg


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()