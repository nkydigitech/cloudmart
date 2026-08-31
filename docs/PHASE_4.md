### PHASE 4 - Database Persistence for Checkout

**Goal:** Checkout saves orders permanently in PostgreSQL, not localStorage.

**Repo:** https://github.com/nkydigitech/cloudmart | Branch main | Commit f2b9294+

#### Architecture
Frontend (nginx:alpine) :80
  -> /api/products -> product-service ClusterIP 10.98.134.37 :80 [2 pods]
  -> /api/orders -> order-service ClusterIP 10.104.204.248 :80 [2 pods]
       -> postgres-service 10.106.147.1 :5432 -> postgres-0 StatefulSet
            -> PVC postgres-pvc Bound pvc-f1d35e0b-7787-437d-a95f-dfcf897d4803 1Gi RWO standard

#### Step 1 - PostgreSQL
Files: gitops/apps/postgres/secret.yaml (password=cloudmart123), storage.yaml (PVC 1Gi standard), statefulset.yaml (postgres:15, port 5432)
Deploy: kubectl apply -f gitops/apps/postgres/
Verify:
- kubectl get pods -n dev => postgres-0 1/1 Running (your screenshot 7m43s)
- kubectl get pvc -n dev => postgres-pvc Bound 1Gi (your screenshot 10m)
- kubectl get statefulset -n dev => postgres 1/1 12m
- kubectl get svc -n dev => postgres None 5432, postgres-service 10.106.147.1 5432

#### Step 2 - Order Service
Files: apps/order-service/main.py (FastAPI, CREATE TABLE IF NOT EXISTS orders, GET /, /health, POST /orders, GET /orders), Dockerfile python:3.11-slim, requirements.txt fastapi psycopg2-binary uvicorn, gitops/apps/order-service/deployment.yaml (2 replicas, DB_HOST=postgres-service.dev.svc.cluster.local)
Deploy: kubectl apply -f gitops/apps/order-service/
Verify: kubectl get pods -n dev => order-service-cc9cc955-nmm2k 1/1, swrd9 1/1

Fix: kubectl exec -it postgres-0 -n dev -- psql -U cloudmart -d cloudmartdb -c "CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, user_email VARCHAR(255), user_name VARCHAR(255), total INTEGER, items JSONB, created_at TIMESTAMP DEFAULT NOW());"

#### Step 3 - Connect & Verify (Your real outputs)
Port-forward:
kubectl port-forward svc/frontend 8080:80 -n dev --address=0.0.0.0 &
kubectl port-forward svc/order-service 8082:80 -n dev --address=0.0.0.0 &
kubectl port-forward svc/product-service 8081:80 -n dev --address=0.0.0.0 &
PORTS tab -> globe icon

Test:
curl -X POST http://localhost:8082/orders -H "Content-Type: application/json" -d '{"user_email":"nkechi@test.com","user_name":"Nkechi","total":50000,"items":[{"name":"Laptop"}]}'
=> {"id":1,"user_email":"nkechi@test.com","user_name":"Nkechi","total":50000,"items":[{"name":"Laptop"}],"created_at":"2026-08-31T19:56:41.416787"}

curl http://localhost:8082/orders
=> [{"id":1,"user_email":"nkechi@test.com","user_name":"Nkechi","total":50000,"items":[{"name":"Laptop"}],"created_at":"2026-08-31T19:56:41.416787"}]

kubectl exec -it postgres-0 -n dev -- psql -U cloudmart -d cloudmartdb -c "SELECT * FROM orders;"

#### Step 4 - Ingress
kubectl get ingress -n dev => 2 ingress ADDRESS 192.168.49.2
/ -> frontend 80, /api/orders -> order-service 80, /api/products -> product-service 80
Your screenshots: ingress.yaml.png, kubectl_get_svc, etc.

#### Step 5 - GitOps & ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd => 7 pods Running (your screenshot argocd.png)
kubectl port-forward svc/argocd-server -n argocd 8083:80 --address=0.0.0.0 & => admin / napOIWOYIitpQUcx

Git push: git push origin main - 26 objects, 4.89 KiB

#### Tech Stack Phase 4 Real Values
DB: postgres:15 StatefulSet postgres-0 not Deployment, Storage PVC 1Gi standard RWO, Service order-service Python 3.11 FastAPI + psycopg2, Secret postgres-secret password cloudmart123, Namespace dev + argocd

#### Screenshots Evidence
argocd.png, kubectl_get_pvc, statefulset, svc, pods, ingress.yaml, port_forwarding, product.png + curl success
