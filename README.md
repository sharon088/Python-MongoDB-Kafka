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


### MongoDB configuration
    mongo:
        enabled: true
        replicaCount: 1
        image:
            repository: mongo
            tag: "latest"
        service:
            name: mongo
            port: 27017
        auth:
            secretName: mongo-credentials
        persistence:
            enabled: true
            size: 1Gi

### Consumer Configuration
    consumer:
        enabled: true
        replicaCount: 1
        image:
            repository: sharon088/kafka_mongo_flask-consumer
            tag: "latest"
        kafka:
            bootstrapServer: "broker:9092"  # Kafka bootstrap server
        containerPort: 6000

### Default Values for the App
    replicaCount: 1
    image:
        repository: sharon088/kafka_mongo_flask-app
        pullPolicy: IfNotPresent
        tag: "latest"

    service:
        type: NodePort
        port: 5000
        targetPort: 5000
        protocol: TCP

    resources: {}

### MongoDB Persistent Volume Configuration
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
        name: mongo-pvc
    spec:
        accessModes:
            - ReadWriteOnce
    resources:
        requests:
            storage: 1Gi

### Kafka Service Configuration
    apiVersion: v1
    kind: Service
    metadata:
        name: broker
    spec:
    ports:
        - port: 9092
        targetPort: 9092
        protocol: TCP
    selector:
        app: broker
    type: ClusterIP

### Flask Consumer Service Configuration
    apiVersion: v1
    kind: Service
    metadata:
        name: consumer
    spec:
    ports:
        - port: 6000
        targetPort: 6000
    selector:
        app: consumer

## Secrets Configuration
    This Helm chart expects a Kubernetes secret for MongoDB credentials, which can be created using the following command:
    ```bash
    kubectl create secret generic mongo-credentials \
  --from-literal=MONGO_INITDB_ROOT_USERNAME=<your-username> \
  --from-literal=MONGO_INITDB_ROOT_PASSWORD=<your-password>
    ```

## Deployment Strategy
By default, this chart sets a replica count of 1 for the MongoDB, Kafka, and Flask consumer services. You may want to scale these services depending on your production needs.

```bash
    replicaCount: 3
```
Ensure the correct scaling is set for high availability and fault tolerance.

## Liveness and Readiness Probes
Liveness and readiness probes are configured in the values.yaml file to ensure the health of your pods. You can customize them based on your application's health check endpoint.

```bash
    livenessProbe:
    httpGet:
        path: /health
        port: 5000
    readinessProbe:
    httpGet:
        path: /health
        port: 5000
```

## Troubleshooting
If you encounter any issues with the deployment, check the logs for each service:
- For Kafka:
    ```bash
    kubectl logs <kafka-pod-name>   
    ```

- For MongoDB:
    ```bash
    kubectl logs <mongo-pod-name>

    ```

- For Flask consumer:
    ```bash
    kubectl logs <consumer-pod-name> 
    ```