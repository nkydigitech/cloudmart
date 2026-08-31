![CloudMart Banner](docs/banner.png)

# CloudMart 🛒 - GitOps E-Commerce on Kubernetes

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.29-326CE5?logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)
![ArgoCD](https://img.shields.io/badge/ArgoCD-GitOps-EF4444?logo=argo)
![Status](https://img.shields.io/badge/Status-Phase%203%20Complete-success)

> Cloud-native e-commerce - Minikube, Docker, ArgoCD, NGINX Ingress, FastAPI, Jumia UI with real images, Naira prices, Login/Signup

**Live:** https://nkydigitech.github.io/cloudmart/ | **Notion:** https://app.notion.com/p/CloudMart-DevOps-Cloud-Engineering-Project-3cabda4c72b58094b32ec94ef1a6bb9b

## About Me
**Nkechi Ahanonye** | nkydigitech · she/her | Cloud & DevOps Engineer | I turn manual 3 AM deployments into 1-min pipelines
- LinkedIn: https://www.linkedin.com/in/nkechiahanonye
- GitHub: https://github.com/nkydigitech

## Screenshots
Browser Verified E2E: CloudMart header, Cart, 8 products with images, Naira, discount, ratings, Login modals, API JSON, ArgoCD Synced Healthy

## Architecture
GitHub → ArgoCD → Minikube (dev: frontend 2 + product-service 2, ingress-nginx, argocd)

Flow: Ingress 192.168.49.2 → / → Frontend → fetch /api/products → product-service

## Quick Start
minikube start && minikube addons enable ingress
cd apps/frontend && docker build -t frontend:v2 . && minikube image load frontend:v2
cd ../product-service && docker build -t product-service:v1 . && minikube image load product-service:v1
kubectl apply -f gitops/apps/product-service/deployment.yaml
kubectl apply -f gitops/apps/frontend/deployment.yaml
kubectl apply -f gitops/apps/frontend/ingress.yaml
kubectl get pods -n dev && curl http://$(minikube ip)/api/products
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80 --address=0.0.0.0 &

## GitHub Pages Fix
Pages needs docs/index.html - this repo now includes it. Enable: Settings → Pages → main → /docs

## Fixes
- yaml line 17 → indentation
- /api/products returns service → 2 ingress + backend serves /api/products
- 192.168.49.2 browser → port-forward
- Pages 404 → copy index.html to docs/

## Verification
kubectl get pods -n dev (4 Running)
kubectl get ingress -n dev (192.168.49.2)
kubectl get application -n argocd (Synced Healthy)
curl /api/products → list

Topics: kubernetes docker argocd gitops fastapi minikube devops jumia-clone
Author: Nkechi Ahanonye - Lagos, Nigeria
