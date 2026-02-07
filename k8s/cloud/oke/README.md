# Oracle Cloud OKE Deployment Guide

This guide walks you through deploying the Todo Evolution application to Oracle Container Engine for Kubernetes (OKE).

## Prerequisites

1. **Oracle Cloud Account** - Sign up at [cloud.oracle.com](https://cloud.oracle.com)
   - Free tier includes Always Free resources
   - New accounts get $300 credit

2. **OCI CLI** - Install Oracle Cloud Infrastructure CLI
   ```bash
   # Windows (PowerShell)
   Set-ExecutionPolicy RemoteSigned
   powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1'))"
   
   # macOS/Linux
   bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
   ```

3. **kubectl** - Kubernetes CLI
   ```bash
   # Windows (winget)
   winget install Kubernetes.kubectl
   
   # macOS
   brew install kubectl
   ```

4. **Helm 3** - Kubernetes package manager
   ```bash
   # Windows (winget)
   winget install Helm.Helm
   
   # macOS
   brew install helm
   ```

## Step 1: Configure OCI CLI

```bash
# Configure OCI CLI with your credentials
oci setup config

# Verify configuration
oci iam region list
```

You'll need:
- User OCID (from OCI Console → Profile → User Settings)
- Tenancy OCID (from OCI Console → Profile → Tenancy)
- Region (e.g., us-ashburn-1, uk-london-1)
- API Key (generate during setup)

## Step 2: Create OKE Cluster

### Option A: Quick Create (Recommended)

1. Go to OCI Console → Developer Services → Kubernetes Clusters (OKE)
2. Click "Create Cluster" → "Quick Create"
3. Configure:
   - **Name**: `todo-evolution-cluster`
   - **Kubernetes Version**: Latest (1.28+)
   - **Node Pool Shape**: `VM.Standard.E4.Flex` (1 OCPU, 8GB RAM)
   - **Number of Nodes**: 3
   - **Network**: Public Endpoint, Private Workers

### Option B: Using OCI CLI

```bash
# Set variables
export COMPARTMENT_ID="ocid1.compartment.oc1..your-compartment-id"
export CLUSTER_NAME="todo-evolution-cluster"

# Create VCN for OKE
oci ce cluster create-kubeconfig \
  --cluster-id $CLUSTER_ID \
  --file $HOME/.kube/config \
  --region us-ashburn-1 \
  --token-version 2.0.0
```

## Step 3: Configure kubectl

```bash
# Get cluster access
oci ce cluster create-kubeconfig \
  --cluster-id <your-cluster-ocid> \
  --file $HOME/.kube/config \
  --region <your-region> \
  --token-version 2.0.0

# Verify connection
kubectl get nodes
```

## Step 4: Create Container Registry (OCIR)

```bash
# Get namespace
oci os ns get

# Login to OCIR
docker login <region-code>.ocir.io -u '<tenancy-namespace>/<username>'
# Password: Use Auth Token (generate in OCI Console → Profile → Auth Tokens)

# Tag and push images
docker tag todo-backend:latest <region-code>.ocir.io/<namespace>/todo-backend:latest
docker tag todo-frontend:latest <region-code>.ocir.io/<namespace>/todo-frontend:latest

docker push <region-code>.ocir.io/<namespace>/todo-backend:latest
docker push <region-code>.ocir.io/<namespace>/todo-frontend:latest
```

Region codes:
- `iad` - us-ashburn-1
- `phx` - us-phoenix-1
- `lhr` - uk-london-1
- `fra` - eu-frankfurt-1

## Step 5: Create Kubernetes Secrets

```bash
# Create namespace
kubectl create namespace todo-app

# Create OCIR pull secret
kubectl create secret docker-registry ocir-secret \
  --namespace todo-app \
  --docker-server=<region-code>.ocir.io \
  --docker-username='<tenancy-namespace>/<username>' \
  --docker-password='<auth-token>' \
  --docker-email='<your-email>'

# Create application secrets
kubectl create secret generic todo-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL='postgresql://user:pass@host:5432/db' \
  --from-literal=OPENAI_API_KEY='sk-...' \
  --from-literal=JWT_SECRET='your-jwt-secret'
```

## Step 6: Deploy with Helm

```bash
# Add Helm repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Deploy PostgreSQL (or use Oracle Autonomous Database)
helm install postgres bitnami/postgresql \
  --namespace todo-app \
  --set auth.postgresPassword=todopass \
  --set auth.database=tododb

# Deploy the application
helm upgrade --install todo-app ./helm/todo-app \
  --namespace todo-app \
  --values ./helm/todo-app/values-oke.yaml \
  --set backend.image.repository=<region-code>.ocir.io/<namespace>/todo-backend \
  --set frontend.image.repository=<region-code>.ocir.io/<namespace>/todo-frontend \
  --set imagePullSecrets[0].name=ocir-secret
```

## Step 7: Configure Ingress

### Option A: OCI Load Balancer (Automatic)

```bash
# The LoadBalancer service creates an OCI Load Balancer automatically
kubectl get svc -n todo-app

# Get external IP
kubectl get svc todo-app-frontend -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### Option B: NGINX Ingress Controller

```bash
# Install NGINX Ingress
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.annotations."oci\.oraclecloud\.com/load-balancer-type"="lb" \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape"="flexible" \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape-flex-min"="10" \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/oci-load-balancer-shape-flex-max"="100"

# Apply ingress resource
kubectl apply -f k8s/cloud/oke/ingress.yaml
```

## Step 8: Deploy Dapr on OKE

```bash
# Install Dapr
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

helm install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --set global.mtls.enabled=true

# Apply Dapr components
kubectl apply -f dapr/components/ -n todo-app
```

## Step 9: Deploy Kafka (Strimzi)

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Deploy Kafka cluster
kubectl apply -f k8s/dapr/kafka-cluster.yaml -n kafka

# Wait for Kafka to be ready
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka
```

## Monitoring & Observability

### OCI Monitoring

```bash
# Enable OKE Cluster Metrics
# Go to OCI Console → Observability → Monitoring → Metrics Explorer

# View logs
# Go to OCI Console → Observability → Logging → Logs
```

### Install Prometheus & Grafana

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

## Cleanup

```bash
# Delete application
helm uninstall todo-app -n todo-app

# Delete cluster (from OCI Console or CLI)
oci ce cluster delete --cluster-id <cluster-ocid>
```

## Cost Optimization

1. **Always Free Resources**:
   - 2 AMD-based Compute VMs (1/8 OCPU, 1GB RAM each)
   - 4 Arm-based Ampere A1 cores and 24GB RAM
   - 200GB Block Storage

2. **Flexible Shapes**: Use `VM.Standard.E4.Flex` for pay-as-you-go

3. **Preemptible Instances**: Use for non-critical workloads

4. **Scale Down**: Reduce node count during off-hours

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Image pull errors
```bash
# Verify OCIR secret
kubectl get secret ocir-secret -n todo-app -o yaml

# Check image path
kubectl describe pod <pod-name> -n todo-app | grep Image
```

### Load Balancer not provisioning
```bash
# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'

# Verify annotations
kubectl get svc -n todo-app -o yaml
```
