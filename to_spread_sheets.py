import logging
from quixstreams import Application
from datetime import timedelta
from uuid import uuid4 ## to generate a unique consumer group ID
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def initializer(msg):
    temperature = msg.get("current", {}).get("temperature_2m", None)
    return {"open": temperature,
            "close": temperature,
            "low": temperature,
            "high": temperature}

def reducer(summary, msg):
    temperature = msg.get("current", {}).get("temperature_2m", None)
    return {"open": summary["open"],
            "close": temperature,
            "low": min(summary["low"], temperature),
            "high": max(summary["high"], temperature)}

def main():
    app = Application(broker_address="localhost:9092",
                      loglevel="DEBUG",
                      consumer_group=str(uuid4()),
                      auto_offset_reset="earliest"
                      ) ## identify which application with unique string                   )
    input_topic = app.topic("weather_data_demo")
    sdf = app.dataframe(input_topic) ## create a streaming dataframe from the input topic
    sdf = sdf.tumbling_window(duration_ms=timedelta(hours=1)) ## create a tumbling window of 1 hour in milli secs
    # sdf = sdf.summarize_that_hour() ## summarize the hourly batches

    sdf = sdf.reduce(initializer=initializer,
                     reducer=reducer) ## reduce the streaming dataframe to a single row per hour

    sdf = sdf.final()

    sdf = sdf.update(lambda msg: logging.info(f"Summarized data: {msg}"))  ## log the summarized data
    # sdf = sdf.send_to_google_sheets() ## send the summarized data to Google Sheets

    # sheet_id = "1IpFuLQbkCa8yCU0-U5GQbznEYXARa0HJlv5OiJ2fsVI"
    # # The scope and credentials file
    # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scopes=scope)

    # client = gspread.authorize(creds)
    # sheet = client.open_by_key(sheet_id).worksheet("Weather Data")  # or by name

    # # Example: Append a row
    # sheet.append_row(["2025-08-12T00:00:00", 24.5, 24.5, 19.0, 25.0])

    app.run(sdf)  ## run the application with the streaming dataframe   

    output_topic = app.topic("weather_data_demo_output")
    sdf = sdf.to_topic(output_topic)  ## write the streaming dataframe to the output topic
if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main() 