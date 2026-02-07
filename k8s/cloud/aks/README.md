# Azure AKS Deployment Guide

Deploy the Todo App to Azure Kubernetes Service (AKS).

## Prerequisites

- Azure CLI installed and configured
- kubectl installed
- Helm 3 installed
- Azure subscription

## Quick Start

### 1. Create Resource Group

```bash
az group create --name todo-rg --location eastus
```

### 2. Create AKS Cluster

```bash
az aks create \
  --resource-group todo-rg \
  --name todo-aks \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-addons monitoring \
  --generate-ssh-keys \
  --enable-managed-identity
```

### 3. Get Credentials

```bash
az aks get-credentials --resource-group todo-rg --name todo-aks
```

### 4. Install NGINX Ingress Controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --create-namespace \
  --namespace ingress-nginx \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz
```

### 5. Install cert-manager (for TLS)

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

### 6. Create ClusterIssuer for Let's Encrypt

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
EOF
```

### 7. Install Dapr

```bash
dapr init -k --wait
```

### 8. Install Strimzi Kafka (Optional)

```bash
kubectl create namespace kafka

kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for operator
kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=300s

# Deploy Kafka cluster
kubectl apply -f k8s/dapr/kafka-cluster.yaml
```

### 9. Create Secrets

Create a secret file with your credentials:

```bash
kubectl create namespace todo-app-prod

kubectl create secret generic todo-app-secrets \
  --namespace todo-app-prod \
  --from-literal=DATABASE_URL='postgresql://user:pass@host:5432/db' \
  --from-literal=JWT_SECRET='your-jwt-secret' \
  --from-literal=OPENAI_API_KEY='your-openai-key'
```

### 10. Deploy Application

```bash
helm upgrade --install todo-app ./helm/todo-app \
  --namespace todo-app-prod \
  --values helm/todo-app/values-cloud.yaml \
  --set ingress.host=todo.yourdomain.com
```

## DNS Configuration

1. Get the ingress external IP:
   ```bash
   kubectl get svc -n ingress-nginx ingress-nginx-controller \
     -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
   ```

2. Create an A record in your DNS provider pointing to this IP.

## Monitoring

### Enable Container Insights

Container Insights is already enabled if you used `--enable-addons monitoring`.

View logs in Azure Portal:
1. Go to your AKS cluster
2. Navigate to Monitoring > Logs
3. Run queries like:
   ```kusto
   ContainerLog
   | where ContainerName == "backend"
   | project TimeGenerated, LogEntry
   | order by TimeGenerated desc
   ```

### Prometheus + Grafana (Optional)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

## Cost Optimization

### Use Spot Instances for Non-Production

```bash
az aks nodepool add \
  --resource-group todo-rg \
  --cluster-name todo-aks \
  --name spotnodepool \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --node-count 2
```

### Enable Cluster Autoscaler

```bash
az aks update \
  --resource-group todo-rg \
  --name todo-aks \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5
```

## Cleanup

```bash
# Delete the AKS cluster
az aks delete --resource-group todo-rg --name todo-aks --yes --no-wait

# Delete the resource group (removes all resources)
az group delete --name todo-rg --yes --no-wait
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n todo-app-prod

# Check events
kubectl get events -n todo-app-prod --sort-by='.lastTimestamp'
```

### Ingress Not Working

```bash
# Check ingress
kubectl describe ingress todo-app-ingress -n todo-app-prod

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

### Database Connection Issues

```bash
# Test connection from a pod
kubectl run -it --rm debug --image=postgres:16 --restart=Never -- \
  psql "postgresql://user:pass@host:5432/db"
```
