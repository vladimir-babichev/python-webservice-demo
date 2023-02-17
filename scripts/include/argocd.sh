#!/usr/bin/env bash

# Source common functions
# shellcheck source=/dev/null
source "$(dirname "$(realpath "$0")")/common.sh"

help() {
    cat <<EOF
    To display this help again use this flags:    -h, --help

    Parameters:
    -n, --namespace     Target namespace
EOF
}


while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -n|--namespace)
        namespace="$2"
        shift
        ;;
    -h|--help)
        help
        exit 0
        ;;
    *)
        fail "Parameter $1 not recognized!"
        ;;
  esac
  shift
done

[[ -z "$namespace" ]] && fail "Namespace cannot be null!"

if ! kubectl get ns "$namespace" >/dev/null 2>&1; then
    kubectl create namespace "$namespace"
fi

kubens "$namespace"

cd "${ROOT_DIR}/k8s/gitops/argocd/" || fail
helm repo add argo https://argoproj.github.io/argo-helm  || fail
helm dependency build || fail
helm template argocd . \
    --set argo-cd.server.ingress=null | \
    kubectl apply -f - || fail

kubectl rollout status deploy argocd-server -n "$namespace"
kubectl rollout status deploy argocd-applicationset-controller -n "$namespace"
kubectl rollout status deploy argocd-notifications-controller -n "$namespace"
kubectl rollout status deploy argocd-redis -n "$namespace"
kubectl rollout status deploy argocd-repo-server -n "$namespace"
kubectl rollout status deploy argocd-server -n "$namespace"
