terraform {
  required_version = ">= 1.5.0"
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.25" }
    helm = { source = "hashicorp/helm", version = "~> 2.12" }
  }
}
provider "kubernetes" {
  config_path = "~/.kube/config"
}
provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
resource "kubernetes_namespace" "argocd" {
  metadata { name = "argocd" }
}
resource "kubernetes_namespace" "monitoring" {
  metadata { name = "monitoring" }
}
resource "kubernetes_namespace" "dev" {
  metadata { name = "dev" }
}
resource "helm_release" "argocd" {
  name = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart = "argo-cd"
  namespace = kubernetes_namespace.argocd.metadata[0].name
  version = "6.7.0"
  values = [file("${path.module}/values-argocd.yaml")]
}
resource "helm_release" "monitoring" {
  name = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart = "kube-prometheus-stack"
  namespace = kubernetes_namespace.monitoring.metadata[0].name
  version = "58.0.0"
  values = [file("${path.module}/values-monitoring.yaml")]
  timeout = 600
}
