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
