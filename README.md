## Azure K8s Sidecar Deployment (Local Simulation)

### Prerequisites

Before getting started, ensure you have the following installed on your machine:

- **Docker**: Required to build and run the container images locally.  
- **Minikube** or any local Kubernetes cluster (such as Docker Desktop with Kubernetes enabled): This allows you to simulate deployment and pod behavior as it would run in a real Kubernetes environment.  
- **kubectl**: The Kubernetes command-line tool used to interact with your cluster.

### Running the Application Locally

To simulate the sidecar deployment locally, begin by checking out the appropriate branch:

```bash
git checkout local-branch
```
Start minikube:

```bash
minikube start
```

Next, build the Docker images for the main service and sidecar inside minikube:

```bash
eval $(minikube docker-env) 
docker build -t main-service -f Dockerfile.main .
docker build -t sidecar-service -f Dockerfile.sidecar .
```

Once the images are built, apply the Kubernetes manifests to deploy both services:

```bash
kubectl apply -f k8s/main-deployment.yaml
kubectl apply -f k8s/main-service.yaml
kubectl apply -f k8s/sidecar-deployment.yaml
kubectl apply -f k8s/sidecar-service.yaml
```

To verify everything is up and running, check the status of the pods:

```bash
kubectl get pods
```

You should see output similar to the following, with all pods showing a `RUNNING` status:

```bash
NAME                               READY   STATUS    RESTARTS   AGE
main-service-b8785df5-dz6nc        1/1     Running   0          38s
sidecar-service-5654b56559-659v4   1/1     Running   0          24m
sidecar-service-5654b56559-p85cr   1/1     Running   0          24m
```

For deeper insight, you can inspect logs with `kubectl logs <pod-name>` or get detailed information using `kubectl describe pod <pod-name>`.

To interact with the services, forward the main service to port 5000 and the sidecar service to port 5001 on your local machine:

```bash
kubectl port-forward service/main-service 5000:5000 && kubectl port-forward service/sidecar-service 5001:5000
```

With everything in place, simulate a file download using the following `curl` command:

```bash
curl -X POST http://localhost:5000/download -H "Content-Type: application/json" -d '{"filename": "ecooly.png"}'
```

Depending on the simulated load (randomly generated), the request will either be handled by the main service:

```bash
{"message":"[MAIN SERVICE]: Successfully processed download for ecooly.png. Number of active requests is 25"}
```

Or routed to the sidecar service:

```bash
{"message":"[SIDECAR SERVICE]: Successfully processed download for ecooly.png. Received active requests: 49"}
```

You can repeat the `curl` command multiple times to observe the simulated load balancing in action. Each request reflects how the sidecar pattern can help distribute load dynamically based on current conditions.