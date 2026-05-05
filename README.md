# Bangalore Home Price Prediction

## Project structure

- `frontend/`: static UI (HTML/CSS/JS)
- `backend/`: Flask API + prediction logic
  - `backend/artifacts/`: trained model + `columns.json`
  - `backend/notebooks/`: training notebook(s)
  - `backend/config/`: config files
- `db/`: dataset(s)

## Run backend

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

From the repo root:

```bash
python -m backend.server
```

Or from inside `backend/`:

```bash
python server.py
```

## Docker: build image from Dockerfile

From the folder that contains your `Dockerfile`:

```bash
docker build -t flask-app-home-price-prediction:latest .
```

Verify the image:

```bash
docker images | findstr flask-app-home-price-prediction
```

### (Optional) Push to Docker Hub

```bash
docker login
docker tag flask-app-home-price-prediction:latest <dockerhub-username>/flask-app-home-price-prediction:latest
docker push <dockerhub-username>/flask-app-home-price-prediction:latest
```

## Kubernetes: deploy Docker image

Manifests are in `k8s/`:

- `k8s/namespace.yaml`: creates the `home-price-prediction` namespace
- `k8s/deployment.yaml`: creates:
  - a `Deployment` using the Docker image (`pmshrik/flask-app-home-price-prediction`)
  - a `Service` named `flask-app-service` of type `NodePort` on port `30007`

Apply:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
```

Check status:

```bash
kubectl -n home-price-prediction get pods
kubectl -n home-price-prediction get svc flask-app-service
kubectl -n home-price-prediction get endpoints flask-app-service
```

## How the Service exposes the app

The service in `k8s/deployment.yaml`:

- routes **`port: 5000` → `targetPort: 5000`** to the Flask container
- exposes it externally using **`type: NodePort`** on **`nodePort: 30007`**

## Access the app (kind / minikube / kubeadm)

### kind

In kind, “nodes” are Docker containers, so `NodePort` is **not reachable from your host by default**.

Use port-forward (recommended):

```bash
kubectl -n home-price-prediction port-forward svc/flask-app-service 5000:5000
```

Open: `http://localhost:5000`

If you want `NodePort` (`30007`) to work on your host, create the kind cluster with a port mapping for `30007` (then open `http://localhost:30007`):

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30007
        hostPort: 30007
        protocol: TCP
```

```bash
kind delete cluster
kind create cluster --config kind-config.yaml
```

### minikube

If you set a `NodePort` you can typically access it via the minikube node IP:

```bash
minikube ip
```

Open: `http://<minikube-ip>:30007`

Or use the built-in helper (it prints a URL):

```bash
minikube service -n home-price-prediction flask-app-service --url
```

### kubeadm (or any “real” multi-node cluster)

Use any node’s reachable IP address:

Open: `http://<node-ip>:30007`

Useful commands to get node IPs:

```bash
kubectl get nodes -o wide
```