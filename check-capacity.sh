echo "=== OS ==="
cat /etc/os-release | grep PRETTY
uname -m
echo ""
echo "=== CPU ==="
nproc
lscpu | grep "Model name"
echo ""
echo "=== RAM ==="
free -h
echo ""
echo "=== DISK ==="
df -h | grep -E "Filesystem|/dev/root|overlay"
echo ""
echo "=== DOCKER ==="
docker ps
echo ""
echo "=== MINIKUBE ==="
minikube version
minikube status
