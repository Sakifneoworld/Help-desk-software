# Kubernetes Verification Guide - Planet API

## ✅ Verification Commands

### 1. **Check Pod Status**
```bash
kubectl get pods -n planet-api
```
Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
planet-api-5679575545-s9t8c   1/1     Running   0          5m
planet-api-5679575545-v2mzb   1/1     Running   0          5m
```
- `READY 1/1` = Pod is ready
- `STATUS Running` = Pod is actively running
- `RESTARTS 0` = No crashes/restarts

---

### 2. **Get Detailed Pod Information**
```bash
kubectl describe pod -n planet-api <POD_NAME>
```
Key indicators:
- **Status: Running** ✓
- **Ready: True** ✓
- **Containers Status: Running** ✓
- **Conditions: All True** ✓

---

### 3. **Check Deployment Rollout Status**
```bash
kubectl rollout status deployment/planet-api -n planet-api
```
Expected: `deployment "planet-api" successfully rolled out`

---

### 4. **View Pod Logs**
```bash
# View latest logs from all pods
kubectl logs -n planet-api deployment/planet-api --tail=20

# Follow logs in real-time
kubectl logs -n planet-api deployment/planet-api -f

# View specific pod logs
kubectl logs -n planet-api <POD_NAME>
```
Expected: `INFO: Uvicorn running on http://0.0.0.0:8000`

---

### 5. **Check Health Probes**
```bash
# Liveness probe (is app alive?)
kubectl get pod -n planet-api -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Liveness")].status}{"\n"}{end}'

# Readiness probe (is app ready to serve?)
kubectl get pod -n planet-api -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'
```

---

### 6. **Execute Command Inside Pod**
```bash
# Run Python command
kubectl exec -it -n planet-api <POD_NAME> -- python --version

# Check if app is running
kubectl exec -it -n planet-api <POD_NAME> -- ps aux | grep uvicorn

# Install tools and test
kubectl exec -it -n planet-api <POD_NAME> -- curl http://localhost:8000/health
```

---

### 7. **Check Service & Network**
```bash
# View service details
kubectl get svc -n planet-api

# View ingress
kubectl get ingress -n planet-api

# Test service connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -n planet-api -- curl http://planet-api:80/planet/3
```

---

### 8. **Port Forward & Test API**
```bash
# Forward local port to service
kubectl port-forward -n planet-api svc/planet-api 8001:80

# In another terminal, test
curl http://localhost:8001/planet/3
curl http://localhost:8001/planets
curl http://localhost:8001/health
```

---

### 9. **View All Kubernetes Resources**
```bash
# All resources in planet-api namespace
kubectl get all -n planet-api

# With more details
kubectl get all -n planet-api -o wide
```

---

### 10. **Check Events & Issues**
```bash
# View namespace events
kubectl get events -n planet-api --sort-by='.lastTimestamp'

# Describe deployment (shows events)
kubectl describe deployment planet-api -n planet-api
```

---

## 📊 Status Indicators

| Indicator | Status | Meaning |
|-----------|--------|---------|
| READY 1/1 | ✅ Good | Container is ready |
| READY 0/1 | ❌ Bad | Container not ready |
| STATUS Running | ✅ Good | Pod is running |
| STATUS Pending | ⏳ Waiting | Pod starting up |
| STATUS CrashLoopBackOff | ❌ Bad | App keeps crashing |
| RESTARTS 0 | ✅ Good | No crashes |
| RESTARTS > 0 | ⚠️ Warning | App has restarted |

---

## 🔍 What to Look For

### ✅ Pod is Healthy If:
1. `READY` shows `1/1`
2. `STATUS` shows `Running`
3. `RESTARTS` shows `0`
4. Logs show `Uvicorn running on http://0.0.0.0:8000`
5. Health check returns 200 OK
6. Readiness probe shows `True`
7. Liveness probe shows `True`

### ❌ Pod Has Issues If:
1. `READY` shows `0/1`
2. `STATUS` shows `Pending`, `CrashLoopBackOff`, or `ImagePullBackOff`
3. `RESTARTS` shows increasing numbers
4. Logs show errors
5. Health check returns non-200 status
6. Events show failed probe attempts

---

## 🚀 Quick Verification Script

```bash
#!/bin/bash
echo "=== Kubernetes Verification ==="
echo ""
echo "1. Cluster Status:"
kubectl cluster-info
echo ""
echo "2. Pod Status:"
kubectl get pods -n planet-api
echo ""
echo "3. Deployment Rollout:"
kubectl rollout status deployment/planet-api -n planet-api
echo ""
echo "4. Recent Logs:"
kubectl logs -n planet-api deployment/planet-api --tail=5
echo ""
echo "5. Service Status:"
kubectl get svc -n planet-api
echo ""
echo "6. API Health Check:"
curl -s http://localhost/health
echo ""
echo "=== All Healthy! ✅ ==="
```

Save as `verify.sh` and run:
```bash
chmod +x verify.sh
./verify.sh
```

---

## 📝 Common Issues & Solutions

### Issue: Pod stuck in Pending
**Solution:**
```bash
kubectl describe pod <POD_NAME> -n planet-api
# Look for "Events" section - may show insufficient resources
```

### Issue: CrashLoopBackOff
**Solution:**
```bash
# View logs to see the error
kubectl logs -n planet-api <POD_NAME>

# View previous logs if app keeps restarting
kubectl logs -n planet-api <POD_NAME> --previous
```

### Issue: ImagePullBackOff
**Solution:**
```bash
# Image not found, rebuild it
docker build -t planet-api:latest .

# If using registry, ensure image is pushed
docker push <registry>/planet-api:latest
```

### Issue: Service not accessible
**Solution:**
```bash
# Port-forward to test
kubectl port-forward -n planet-api svc/planet-api 8001:80

# Check if service selector matches pod labels
kubectl get pods -n planet-api --show-labels
kubectl get svc -n planet-api -o wide
```
