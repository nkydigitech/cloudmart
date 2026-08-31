![CloudMart Banner](docs/banner.png)

# CloudMart 🛒 - GitOps E-Commerce Platform on Kubernetes

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.29-326CE5?logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-v1-2496ED?logo=docker&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-GitOps-EF4444?logo=argo&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![NGINX Ingress](https://img.shields.io/badge/Ingress-NGINX-009639?logo=nginx&logoColor=white)
![Status](https://img.shields.io/badge/Status-Phase%203%20Complete-success)

> A cloud-native e-commerce demo built with GitOps principles - Minikube, Docker, ArgoCD, NGINX Ingress, FastAPI, and Jumia/Temu-style UI with real images.

**Live Demo (GitHub Pages):** https://nkydigitech.github.io/cloudmart/  
**Repo:** https://github.com/nkydigitech/cloudmart

---

## 📸 Screenshots

### Browser Verified - E2E Working
- Frontend: CloudMart header, Cart (0), 3 product cards Laptop $1200, Phone $800, Headphones $150
- Jumia Enhanced: 8 products with real images, Naira prices ₦345,000, discount -18%, ratings ★4.5, Official Store badges, Login/Signup modals

---

## 🏗️ Architecture

```
GitHub (main) → ArgoCD watches → Minikube Cluster
                                ├── dev namespace
                                │   ├── frontend (2 replicas) nginx:alpine
                                │   ├── product-service (2 replicas) python:3.11 FastAPI
                                │   ├── Services ClusterIP 80
                                │   └── Ingress: / → frontend, /api/products → product-service
                                ├── ingress-nginx (controller Running)
                                ├── argocd (7 pods, 2 Apps Synced Healthy)
                                └── monitoring (Prometheus + Grafana)
```

**Flow:** User → Ingress 192.168.49.2 → / → Frontend → JS fetch /api/products → Ingress → FastAPI → JSON products

---

## ✨ Features

- ✅ GitOps with ArgoCD (automated prune + selfHeal)
- ✅ 2 replicas frontend + backend (HA)
- ✅ NGINX Ingress routing with rewrite-target: /products
- ✅ Jumia/Temu UI - Unsplash real images, Naira prices, discount badges, ratings
- ✅ Sign In / Sign Up modals, Cart drawer, Flash Sales countdown 12:34:56
- ✅ FastAPI backend serves /products and /api/products with CORS
- ✅ Docker images frontend:v1/v2, product-service:v1 via minikube image load
- ✅ Monitoring: kube-prometheus-stack
- ✅ Full E2E verified: curl /api/products → [{"id":1,"name":"Laptop"...}]

---

## 📁 Project Structure

```
cloudmart/
├── apps/
│   ├── frontend/
│   │   ├── Dockerfile (FROM nginx:alpine COPY index.html)
│   │   └── index.html (Jumia-style with search, account, cart)
│   └── product-service/
│       ├── Dockerfile (python:3.11-slim)
│       ├── main.py (/, /products, /api/products, /health)
│       └── requirements.txt (fastapi, uvicorn)
├── gitops/
│   ├── apps/
│   │   ├── frontend/
│   │   │   ├── deployment.yaml (Deployment + Service)
│   │   │   ├── ingress.yaml (cloudmart-api + cloudmart-frontend)
│   │   │   └── argocd-app.yaml
│   │   └── product-service/
│   │       ├── deployment.yaml
│   │       └── argocd-app.yaml
├── terraform/
├── docs/
│   ├── banner.png
│   └── screenshot-ui.png
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Start cluster
minikube start --memory=4096 --cpus=2
minikube addons enable ingress
kubectl create namespace dev

# 2. Build & load
cd apps/frontend && docker build -t frontend:v1 . && minikube image load frontend:v1
cd ../product-service && docker build -t product-service:v1 . && minikube image load product-service:v1

# 3. Deploy
kubectl apply -f gitops/apps/product-service/deployment.yaml
kubectl apply -f gitops/apps/frontend/deployment.yaml
kubectl apply -f gitops/apps/frontend/ingress.yaml

# 4. ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f gitops/apps/product-service/argocd-app.yaml
kubectl apply -f gitops/apps/frontend/argocd-app.yaml

# 5. Verify
kubectl get pods -n dev  # 4 Running
kubectl get svc -n dev
kubectl get ingress -n dev  # ADDRESS 192.168.49.2
kubectl get application -n argocd  # Synced Healthy x2
curl http://$(minikube ip)/api/products
# [{"id":1,"name":"Laptop","price":1200},{"id":2,"name":"Phone","price":800},{"id":3,"name":"Headphones","price":150}]

# 6. Browser (Codespaces - 192.168.49.2 not accessible externally)
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80 --address=0.0.0.0 &
# PORTS tab → 8080 → Open in Browser → https://<codespace>-8080.app.github.dev/
```

---

## 🌐 GitHub Pages

Enable Pages: Settings → Pages → Source: main branch / (root) → Save

URL: https://nkydigitech.github.io/cloudmart/

Frontend on Pages uses fallback static data.

---

## 🔧 API Endpoints

```
GET /api/products → [{"id":1,"name":"Laptop","price":1200,...}]
GET / → CloudMart HTML
GET /health → {"status":"healthy"}
```

---

## 🐛 Key Fixes (Phase 3)

| Issue | Cause | Fix |
|-------|-------|-----|
| yaml: line 17: did not find expected key | 12 spaces before - name: frontend (should be 6) | echo <base64> \| base64 -d > file |
| curl /api/products returns {"service":...} not list | Ingress rewrite /$2 rewrites to / | 2 Ingress: rewrite-target: /products + backend serves /api/products |
| Browser 192.168.49.2 not working | Minikube IP internal to Codespace | kubectl port-forward ingress-nginx-controller 8080:80 --address=0.0.0.0 |

---

## 📝 Phase 3 Verification

```bash
kubectl get application -n argocd
# frontend Synced Healthy
# product-service Synced Healthy

kubectl get pods -n dev
# frontend-xxxx 1/1 Running (2)
# product-service-xxxx 1/1 Running (2)

kubectl get ingress -n dev
# cloudmart-api nginx * 192.168.49.2 80
# cloudmart-frontend nginx * 192.168.49.2 80

curl http://$(minikube ip)/api/products
# [{"id":1,"name":"Laptop","price":1200}...]
```

---

## 🏷️ Tags

`kubernetes` `docker` `argocd` `gitops` `fastapi` `e-commerce` `minikube` `devops` `ingress-nginx` `python` `cloud-native` `jumia-clone` `temu-clone`

---

## 👤 Author

**Ahans BornChampion Nky** - [@nkydigitech](https://github.com/nkydigitech) - Lagos, Nigeria

---

**⭐ Star this repo!**

## About Description for GitHub (copy to About → Settings)

```
CloudMart - GitOps E-Commerce Platform on Kubernetes | Minikube, Docker, ArgoCD, NGINX Ingress, FastAPI, Jumia-style UI with real images, Naira prices, Login/Signup | DevOps Phase 1-3 Complete - Full E2E working with 2 replicas, Ingress routing, ArgoCD Synced Healthy
```
