#!/usr/bin/env bash
# ==============================================================================
# Setup & Deploy ArgoCD for realtime-mlops (kind-churn-model)
# ==============================================================================

set -euo pipefail

echo "==> Step 1: Creating 'argocd' namespace..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo "==> Step 2: Installing ArgoCD components..."
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "==> Step 3: Waiting for ArgoCD Server to be ready..."
kubectl rollout status deployment/argocd-server -n argocd --timeout=300s
kubectl rollout status deployment/argocd-repo-server -n argocd --timeout=300s

echo "==> Step 4: Applying realtime-mlops Application manifest..."
kubectl apply -f "$(dirname "$0")/application.yaml"

echo "==> Step 5: Retrieving ArgoCD initial admin password..."
ADMIN_PWD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" 2>/dev/null | base64 -d || echo "Password already rotated or unavailable yet")

echo "=========================================================="
echo "  ArgoCD Deployment Complete!                             "
echo "=========================================================="
echo "  Username: admin"
echo "  Password: $ADMIN_PWD"
echo ""
echo "To access the ArgoCD Web UI:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "  Open: https://localhost:8080"
echo "=========================================================="
