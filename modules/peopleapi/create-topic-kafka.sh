# Get the name of a Kafka broker pod (assuming it's named "kafka-0")
KAFKA_POD_NAME=my-release-kafka-controller-0

# Enter the Kafka pod using kubectl exec
kubectl exec -it $KAFKA_POD_NAME bash

# Inside the pod, use kafka-topics.sh to create your topic
/opt/kafka/bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092  # Replace with your configuration

# Exit the pod (press Ctrl+d)