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