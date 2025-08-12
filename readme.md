brew install kafka
brew install zookeeper    
brew services start zookeeper
brew services start kafka

## OR

docker run -d --name zookeeper -p 2181:2181 zookeeper:3.9
docker run -d --name kafka -p 9092:9092 --env KAFKA_ZOOKEEPER_CONNECT=host.docker.internal:2181 --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 wurstmeister/kafka


## OR

docker run -p 9092:9092 apache/kafka:latest


## OR

docker run -p 9092:9092 docker.redpanda.com/redpandadata/redpanda:latest \
  redpanda start --overprovisioned --node-id 0 --check=false \
  --kafka-addr 0.0.0.0:9092

## to view logs
kafka-console-consumer --bootstrap-server localhost:9092 --topic weather_data_demo --from-beginning

k-cat -b localhost:9092 -C -t weather_data_demo -o end 

## get redpanda 
brew install redpanda-data/tap/redpanda

rpk redpanda start --dev

which rpk


Got it — you want to run that **Quix Streams** Kafka code but use **Redpanda** as the broker instead of a regular Kafka installation.

Here’s what you need to do:

---

## **1️⃣ Start Redpanda in Dev Mode**

If you still have installation issues with `brew`, I recommend using Docker because it’s much faster and avoids the Xcode problem.

Run this in your terminal:

```bash
docker run -d --name=redpanda \
  -p 9092:9092 \
  -p 9644:9644 \
  docker.redpanda.com/redpandadata/redpanda:latest \
  redpanda start \
  --overprovisioned \
  --smp 1 \
  --memory 1G \
  --reserve-memory 0M \
  --node-id 0 \
  --check=false \
  --kafka-addr PLAINTEXT://0.0.0.0:9092 \
  --advertise-kafka-addr PLAINTEXT://localhost:9092
```

This:

* Starts Redpanda broker at `localhost:9092`
* Runs in **dev mode** with minimal resource usage
* Makes it Kafka API–compatible for your code

---

## **2️⃣ Create the Topics**

Your Python code expects:

* `weather_data_demo`
* `weather_data_demo_output`

Run:

```bash
docker exec -it redpanda rpk topic create weather_data_demo
docker exec -it redpanda rpk topic create weather_data_demo_output
```

---

## **3️⃣ Install Dependencies**

Your Python script uses **Quix Streams**:

```bash
pip install quixstreams
```

---

## **4️⃣ Run Your Code**

Since `broker_address="localhost:9092"` is already set in your code, it should just work:

```bash
python main.py
```

---

## **5️⃣ (Optional) Produce Test Messages**

You can use `rpk` inside the container:

```bash
docker exec -it redpanda rpk topic produce weather_data_demo
```

Type a test JSON or string, then press **Ctrl+D** to send it.

---

If you still prefer **Homebrew install** instead of Docker, you’ll first have to update Xcode CLI tools so `brew install redpanda` can work.

---

I can also give you a **one-liner command** to start Redpanda and auto-create those topics without separate commands — would you like that?
