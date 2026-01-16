# Random Phrase API

Generates random phrases from the phrases.txt file for the frontend_api.py app.

## Requirements

- create a docker network called `app-net`

```bash
docker network create app-net
```

## Docker Commands

### Build container

```bash
docker build . -t backend:v1
```

### Create app-net network

```bash
docker network create app-net
```

### Run container in app-net network

```bash
docker run -d --rm --name backend -p 7070:7070 -h backend --network app-net <container image>
```

## Kubernetes Kind deployment configuration

### Create the phrase namespace

```bash
kubectl create namespace phrase
```

### Copy images from docker to kind

```bash
kind load docker-image backend:v1 backend:v1 --name gwkc-1

Image: "backend:v1" with ID "sha256:7704fd8be7cd9b00459c7f16710e7fd7143217ed5c56b4884938640f3eba2506" not yet present on node "gwkc-1-worker3", loading...
Image: "backend:v1" with ID "sha256:7704fd8be7cd9b00459c7f16710e7fd7143217ed5c56b4884938640f3eba2506" not yet present on node "gwkc-1-worker2", loading...
Image: "backend:v1" with ID "sha256:7704fd8be7cd9b00459c7f16710e7fd7143217ed5c56b4884938640f3eba2506" not yet present on node "gwkc-1-control-plane", loading...
Image: "backend:v1" with ID "sha256:7704fd8be7cd9b00459c7f16710e7fd7143217ed5c56b4884938640f3eba2506" not yet present on node "gwkc-1-worker", loading...
```

### Deploy app

You must have kustomize installed for this step.

```bash
brew install kustomize
```

Deploy application.

```bash
kubectl apply -k -n phrases kube/kustomize/base

service/backend configured
deployment.apps/backend configured
httproute.gateway.networking.k8s.io/backend configured
```

### Verify app

```bash
kubectl get all -n phrases

NAME                          READY   STATUS    RESTARTS   AGE
pod/backend-c6b6d64bc-dzqj2   1/1     Running   0          7m52s
pod/backend-c6b6d64bc-jcd79   1/1     Running   0          7m52s

NAME              TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/backend   ClusterIP   10.96.37.56   <none>        7070/TCP   7m53s

NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/backend   2/2     2            2           7m52s

NAME                                DESIRED   CURRENT   READY   AGE
replicaset.apps/backend-c6b6d64bc   2         2         2       7m52s
% kubectl get httproute -n phrases
NAME      HOSTNAMES           AGE
backend   ["phrases.local"]   8m1s
```

Open [http://phrases.local/backend/random_phrase](http://phrases.local/backend/random_phrase.)
