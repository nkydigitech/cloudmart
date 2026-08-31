# CloudMart 🛒 - GitOps E-Commerce on Kubernetes
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5) ![Docker](https://img.shields.io/badge/Docker-2496ED) ![ArgoCD](https://img.shields.io/badge/ArgoCD-Synced-Healthy-brightgreen) ![Status](https://img.shields.io/badge/Phase%204-DONE-success)

Cloud-native e-commerce - Minikube, Docker, ArgoCD, NGINX Ingress, FastAPI, PostgreSQL 15, Jumia UI with real images, Naira prices, Login/Signup, Persistent Checkout

**Live:** https://nkydigitech.github.io/cloudmart/ | **Notion:** https://app.notion.com/p/CloudMart-DevOps-Cloud-Engineering-Project-3cabda4c72b58094b32ec94ef1a6bb9b | **Repo:** https://github.com/nkydigitech/cloudmart

### About Me
**Nkechi Ahanonye | nkydigitech · she/her | Cloud & DevOps Engineer | I turn manual 3 AM deployments into 1-min pipelines**
- LinkedIn: https://www.linkedin.com/in/nkechiahanonye
- GitHub: https://github.com/nkydigitech

---

### Screenshots - Browser Verified E2E
CloudMart header, Cart, 8 products with images, Naira ₦, discount, ratings, Login modals, API JSON, ArgoCD Synced Healthy + 46 evidence screenshots
- Phase 1: `docs/screenshots/phase1/` (7 files)
- Phase 2: `docs/screenshots/phase2/` (15 files)  
- Phase 3: `docs/screenshots/phase3/` (10 files)
- Phase 4: `docs/screenshots/phase4/` (14 files) → [View all](https://github.com/nkydigitech/cloudmart/tree/main/docs/screenshots)

### Architecture
```
GitHub → ArgoCD → Minikube
  dev namespace:
    frontend 2 replicas (NGINX - Jumia UI)
    product-service 2 replicas ClusterIP 10.98.134.37:80
    order-service 2 replicas ClusterIP 10.104.204.248:80 [NEW Phase 4]
    postgres-0 StatefulSet 1/1 + PVC 1Gi Bound pvc-f1d35e0b... standard
    ingress-nginx-controller
  argocd namespace: 7 pods

Flow:
Browser → Ingress 192.168.49.2
  / → Frontend → fetch /api/products → product-service
  /api/products → product-service
  /api/orders → order-service → postgres-service 10.106.147.1:5432 → postgres-0 → PVC
```

---

## 📚 Phases - From Zero to Persistent Checkout (In Order)

### Phase 1 - Setup [DONE]
Terraform provisions ArgoCD + Prometheus, Minikube, namespaces dev, argocd, monitoring, ingress-nginx
- `kubectl get ns`, `get pods -A`, `current remote`, `ls terraform`, product image
- **Evidence:** `docs/screenshots/phase1/` - current remote.png, get ns.png, get pods -A.png, get pods argocd.png, grt pods monitoring.png, ls terraform.png

### Phase 2 - Backend & Product Service [DONE]
Product Service Deployment 2 replicas, Service ClusterIP, Docker build `product-service:v1`, health checks
- `docker build`, `minikube image load`, `curl /health`, `curl /products`
- ArgoCD Application Synced Healthy
- **Evidence:** `docs/screenshots/phase2/` - 01-ansible-version.png, 05-kubectl-get-pods-dev.png, 06-kubectl-get-svc-dev.png, 10-curl-health.png, 11-curl-products.png, tree architecture.png, watch argocd.png

### Phase 3 - Frontend & Ingress [DONE - E2E Complete]
Frontend NGINX Jumia UI with real images, Naira prices, Login/Signup modals, Ingress fixes
- Fixed: yaml line 17 indentation, /api/products returns service → added 2nd ingress, backend serves /api/products
- 192.168.49.2 browser → port-forward workaround
- Pages 404 → copy index.html to docs/index.html + .nojekyll
- **Evidence:** `docs/screenshots/phase3/` - 01-frontend-html.png, browser.png, frontend deployment.png, ingress -n dev.png, website.png, product-service running.png

### Phase 4 - Database Persistence [CURRENT - DONE] ⭐
**Problem:** Checkout was localStorage → vanished on refresh. No real orders.

**Solution:**
- PostgreSQL 15 as **StatefulSet** postgres-0 1/1 Running (NOT Deployment) - keeps identity & storage
- PVC postgres-pvc Bound 1Gi RWO standard `pvc-f1d35e0b-7787-437d-a95f-dfcf897d4803` 1Gi
- Secret postgres-secret password=cloudmart123
- Order Service FastAPI + psycopg2, python:3.11-slim, auto `CREATE TABLE IF NOT EXISTS orders`, 2 replicas, DB_HOST=postgres-service.dev.svc.cluster.local
- Ingress updated: `/` → frontend 80, `/api/products` → product-service 80, `/api/orders` → order-service 80
- **Painful Fix:** postgres slower than order-service → `relation orders does not exist` → added init check + manual psql CREATE

**Verification (Real outputs from your terminal):**
```bash
POST → {"id":1,"user_email":"nkechi@test.com","user_name":"Nkechi","total":50000,"items":[{"name":"Laptop"}]}
GET /orders → [{"id":1,"user_email":"nkechi@test.com","total":50000,"created_at":"2026-08-31T19:56:41.416787"}]
kubectl exec -it postgres-0 -n dev -- psql -U cloudmart -d cloudmartdb -c "SELECT * FROM orders;"
```
That is persistence - survives pod restart.

**Evidence:** `docs/screenshots/phase4/` (14 files)
- kubectl get pods -n dev.png (6 Running)
- kubectl get pvc -n dev.png (Bound)
- kubectl get svc -n dev.png (postgres-service 10.106.147.1:5432)
- kubectl get statefulset -n dev.png (1/1)
- kubectl get ingress -n dev.png (192.168.49.2)
- kubectl portforward svc orderservice 800180 -n dev.png
- port forwarding.png, product.png, argocd.png, check.png, tree.png

Full doc: [docs/PHASE_4.md](docs/PHASE_4.md)

---

### Quick Start (Phase 1-4)
```bash
minikube start && minikube addons enable ingress

# Phase 4 - DB first
kubectl apply -f gitops/apps/postgres/

# Phase 2-4 - Services
cd apps/product-service && docker build -t product-service:v1 . && minikube image load product-service:v1
cd ../order-service && docker build -t order-service:v1 . && minikube image load order-service:v1
cd ../frontend && docker build -t frontend:v2 . && minikube image load frontend:v2

kubectl apply -f gitops/apps/product-service/deployment.yaml
kubectl apply -f gitops/apps/order-service/deployment.yaml
kubectl apply -f gitops/apps/frontend/deployment.yaml
kubectl apply -f gitops/apps/frontend/ingress.yaml

# Verify
kubectl get pods,svc,pvc,statefulset,ingress -n dev
kubectl get application -n argocd # Synced Healthy
curl http://$(minikube ip)/api/products
curl -X POST http://$(minikube ip)/api/orders -H "Content-Type: application/json" -d '{"user_email":"test@test.com","user_name":"Test","total":1000,"items":[]}'

# Browser
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80 --address=0.0.0.0 &
# PORTS tab → 8080
```

### GitHub Pages Fix
Pages needs `docs/index.html` - this repo includes it. Enable: Settings → Pages → main → /docs
File: `index.html` copied to `docs/index.html` + `.nojekyll`

### Fixes Applied Across Phases
- yaml line 17 → indentation fixed
- /api/products returns service → 2 ingress + backend serves /api/products
- 192.168.49.2 browser → port-forward workaround
- Pages 404 → copy index.html to docs/
- Phase 4: relation orders does not exist → CREATE TABLE IF NOT EXISTS

### Verification
```bash
kubectl get pods -n dev # Phase 4: 6 Running (frontend 2, product 2, order 2, postgres 1)
kubectl get pvc -n dev # Bound 1Gi
kubectl get ingress -n dev # 192.168.49.2
kubectl get application -n argocd # Synced Healthy
curl /api/products → list
curl /api/orders → [{"id":1,...}] persisted
```

### Repository files
- ansible/ - Phase 1 Terraform provisions ArgoCD + Prometheus
- apps/frontend, product-service, order-service
- docs/screenshots/phase1-4/ (46 files) + PHASE_4.md + index.html
- gitops/apps/ - postgres, frontend, product-service, order-service, ingress
- terraform/
- index.html - Jumia UI

Topics: kubernetes docker argocd gitops fastapi minikube devops jumia-clone postgres statefulset pvc
Author: Nkechi Ahanonye - Lagos, Nigeria - 43
