# CloudMart - GitOps E-Commerce Platform

Minikube + ArgoCD + Microservices (Frontend, Product, Order + Postgres)

## Live Demo (Codespace)
- Frontend: PORTS 8080 -> Welcome to nginx!
- Product: PORTS 8081 -> {"service":"product-service","status":"running"}
- Order: PORTS 8082/orders -> [{"id":1,...}]
- ArgoCD: PORTS 8083 -> admin / napOIWOYIitpQUcx

## Architecture
Frontend → product-service → order-service → postgres-0 (StatefulSet + PVC 1Gi)

## Phases
### Phase 4 - Database Persistence [CURRENT - DONE]
- Postgres StatefulSet postgres-0 1/1, PVC Bound 1Gi standard
- Order Service FastAPI 2 replicas, auto-creates orders table
- Ingress 192.168.49.2, / → frontend, /api/orders → order-service
- Verification: POST /orders returns id:1 persisted
- Screenshots: kubectl_get_pods, pvc, svc, statefulset, argocd, port_forwarding, product

See full doc: docs/PHASE_4.md

### Phase 3, 2, 1 ... (keep your old content)

## Tech Stack
K8s 1.28 Minikube, Docker, FastAPI, PostgreSQL 15, ArgoCD, GitOps

## How to Run
kubectl apply -f gitops/apps/postgres/
kubectl apply -f gitops/apps/
kubectl port-forward ...

## Repo
https://github.com/nkydigitech/cloudmart
