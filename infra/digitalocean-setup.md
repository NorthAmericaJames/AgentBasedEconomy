# DigitalOcean Setup Guide

This document provides high‑level instructions for deploying the Evolutionary AI
Ecosystem on DigitalOcean infrastructure as described in the research proposal.
It assumes familiarity with Kubernetes, Docker, and the DigitalOcean control
panel.

## Prerequisites

- A DigitalOcean account with sufficient credits.
- A Kubernetes cluster provisioned via DigitalOcean Kubernetes (DOKS).
- Docker installed locally for building container images.
- `kubectl` configured to point to your DOKS cluster.

## Steps

1. **Build and push the container image**

   ````bash
   # Clone the repository and navigate into it
   git clone <repo-url>
   cd <repo>

   # Build the Docker image
   docker build -t your-dockerhub-username/evo-ai:latest -f evo_ai/infra/Dockerfile .

   # Push to Docker Hub (ensure you're logged in)
   docker push your-dockerhub-username/evo-ai:latest
   ````

2. **Deploy the Ray cluster (optional)**

   If you plan to use Ray for distributed execution, apply the provided
   `ray-cluster.yaml` manifest:

   ```bash
   kubectl apply -f evo_ai/infra/ray-cluster.yaml
   ```

   Monitor the cluster status with:

   ```bash
   kubectl get pods -l rayClusterName=evo-ai-ray
   ```

3. **Deploy the application**

   Apply the Kubernetes deployment manifest:

   ```bash
   kubectl apply -f evo_ai/infra/k8s-manifests/deployment.yaml
   ```

   Expose the service using a LoadBalancer or Ingress, depending on your setup.

4. **Access the dashboard**

   Once deployed, you can access the Streamlit dashboard on the exposed
   service port (default 8501).  Use the DigitalOcean console or `kubectl
   port-forward` to access the service locally for testing.

5. **Configure persistence (optional)**

   For production deployments, configure persistent volumes for agent state,
   Postgres, and Redis.  These are not included in the initial scaffold.

6. **Scaling and monitoring**

   Adjust the replica counts in the deployment manifest and Ray cluster
   specifications to scale your system.  Use Prometheus and Grafana to
   monitor resource usage and agent performance as described in the research
   paper【151713287013870†screenshot】.

## Next Steps

- Implement persistent storage for agent memories and economic ledgers.
- Automate deployment with GitHub Actions.
- Configure autoscaling policies for the Ray cluster.
- Set up metrics dashboards for tithing pools and agent fitness.
