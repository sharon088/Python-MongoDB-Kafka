# Kafka, MongoDB, and Flask Consumer Helm Chart

This Helm chart deploys a Kafka broker, MongoDB, and a Flask consumer application that reads data from Kafka and stores it in MongoDB. This setup is designed for Kubernetes environments and leverages Helm for simplified installation and management.

## Prerequisites

- Kubernetes cluster (e.g., Minikube, GKE, EKS, etc.)
- Helm 3.x or later
- Docker (for building custom images)

## Architecture

- **Kafka**: Acts as the messaging system.
- **MongoDB**: Stores data processed by the Flask consumer.
- **Flask Consumer**: A Flask application that consumes Kafka messages and stores them in MongoDB.

## Installation

1. **Add the Helm repository (if you're using a custom Helm chart repository):**

   If you're using a custom chart repository, add it with the following command:
   ```bash
   helm repo add <your-repo-name> <your-repo-url>
   helm repo update
   ```

2. **Clone this repository:**
    ```bash
    git clone <repo-url>
    cd <repo-directory>
    ```
3. **Install the Helm chart: You can install this Helm chart by using the following command:**
    ```bash
    helm install <release-name> .
    ```
    Replace <release-name> with your desired Helm release name.


## Configuration
You can configure the chart using the values.yaml file. Below are some of the key configuration options:

### Kafka configuration
    ```bash
    kafka:
    enabled: true
    image:
        repository: apache/kafka
        tag: latest
    service:
        name: broker
        port: 9092
    config:
        KAFKA_NODE_ID: 1
        KAFKA_PROCESS_ROLES: "broker,controller"
        KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:9092,CONTROLLER://localhost:9093"
        KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://broker:9092"
        KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
        KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT"
        KAFKA_CONTROLLER_QUORUM_VOTERS: "1@localhost:9093"
        KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
        KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
        KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
        KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
        KAFKA_NUM_PARTITIONS: 3
    ```