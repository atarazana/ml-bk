# Setup your python virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

# Install the dependencies

```sh
pip install -r requirements.txt
```

# Train with

```sh
./run-train.sh
```

# Deploy

```sh
oc login ...
```

```sh
cd deploy
./deploy.sh
```

# Manually deploying ml-bk

Create a new project in your OpenShift cluster.

Running this:

```sh
oc create secret generic ml-models --from-file=../models/model.joblib -n ${DEPLOYMENT_NS} --dry-run=client -o yaml > all.yaml
```

You get this:

> Copy this and deploy it to the project you just created:

```yaml
apiVersion: v1
kind: Secret
data:
  model.joblib: gASVKQUAAAAAAACMEHNrbGVhcm4ucGlwZWxpbmWUjAhQaXBlbGluZZSTlCmBlH2UKIwFc3RlcHOUXZQojAtwcmVwYXJhdGlvbpSMI3NrbGVhcm4uY29tcG9zZS5fY29sdW1uX3RyYW5zZm9ybWVylIwRQ29sdW1uVHJhbnNmb3JtZXKUk5QpgZR9lCiMDHRyYW5zZm9ybWVyc5RdlCiMA251bZRoAimBlH2UKGgFXZQojAdpbXB1dGVylIwUc2tsZWFybi5pbXB1dGUuX2Jhc2WUjA1TaW1wbGVJbXB1dGVylJOUKYGUfZQojA5taXNzaW5nX3ZhbHVlc5RHf/gAAAAAAACMDWFkZF9pbmRpY2F0b3KUiYwTa2VlcF9lbXB0eV9mZWF0dXJlc5SJjAhzdHJhdGVneZSMBm1lZGlhbpSMCmZpbGxfdmFsdWWUTowEY29weZSIjBBfc2tsZWFybl92ZXJzaW9ulIwFMS4zLjGUdWKGlIwNYXR0cmlic19hZGRlcpSMEXV0aWwudHJhbnNmb3JtZXJzlIwXQ29tYmluZWRBdHRyaWJ1dGVzQWRkZXKUk5QpgZR9lIwVYWRkX2JlZHJvb21zX3Blcl9yb29tlIhzYoaUjApzdGRfc2NhbGVylIwbc2tsZWFybi5wcmVwcm9jZXNzaW5nLl9kYXRhlIwOU3RhbmRhcmRTY2FsZXKUk5QpgZR9lCiMCXdpdGhfbWVhbpSIjAh3aXRoX3N0ZJSIaB+IaCBoIXVihpRljAZtZW1vcnmUTowHdmVyYm9zZZSJaCBoIXViXZQojAlsb25naXR1ZGWUjAhsYXRpdHVkZZSMEmhvdXNpbmdfbWVkaWFuX2FnZZSMC3RvdGFsX3Jvb21zlIwOdG90YWxfYmVkcm9vbXOUjApwb3B1bGF0aW9ulIwKaG91c2Vob2xkc5SMDW1lZGlhbl9pbmNvbWWUZYeUjANjYXSUjB9za2xlYXJuLnByZXByb2Nlc3NpbmcuX2VuY29kZXJzlIwNT25lSG90RW5jb2RlcpSTlCmBlH2UKIwKY2F0ZWdvcmllc5SMBGF1dG+UjAZzcGFyc2WUjApkZXByZWNhdGVklIwNc3BhcnNlX291dHB1dJSIjAVkdHlwZZSMBW51bXB5lIwHZmxvYXQ2NJSTlIwOaGFuZGxlX3Vua25vd26UjAVlcnJvcpSMBGRyb3CUTowNbWluX2ZyZXF1ZW5jeZROjA5tYXhfY2F0ZWdvcmllc5ROjBVmZWF0dXJlX25hbWVfY29tYmluZXKUjAZjb25jYXSUaCBoIXViXZSMD29jZWFuX3Byb3hpbWl0eZRhh5RljAlyZW1haW5kZXKUaFGMEHNwYXJzZV90aHJlc2hvbGSURz/TMzMzMzMzjAZuX2pvYnOUTowTdHJhbnNmb3JtZXJfd2VpZ2h0c5ROaDWJjBl2ZXJib3NlX2ZlYXR1cmVfbmFtZXNfb3V0lIiMEWZlYXR1cmVfbmFtZXNfaW5flIwTam9ibGliLm51bXB5X3BpY2tsZZSMEU51bXB5QXJyYXlXcmFwcGVylJOUKYGUfZQojAhzdWJjbGFzc5RoTIwHbmRhcnJheZSTlIwFc2hhcGWUSwmFlIwFb3JkZXKUjAFDlGhLaEyMBWR0eXBllJOUjAJPOJSJiIeUUpQoSwOMAXyUTk5OSv////9K/////0s/dJRijAphbGxvd19tbWFwlImMG251bXB5X2FycmF5X2FsaWdubWVudF9ieXRlc5RLEHVigAJjbnVtcHkuY29yZS5tdWx0aWFycmF5Cl9yZWNvbnN0cnVjdApxAGNudW1weQpuZGFycmF5CnEBSwCFcQJjX2NvZGVjcwplbmNvZGUKcQNYAQAAAGJxBFgGAAAAbGF0aW4xcQWGcQZScQeHcQhScQkoSwFLCYVxCmNudW1weQpkdHlwZQpxC1gCAAAATzhxDImIh3ENUnEOKEsDWAEAAAB8cQ9OTk5K/////0r/////Sz90cRBiiV1xEShYCQAAAGxvbmdpdHVkZXESWAgAAABsYXRpdHVkZXETWBIAAABob3VzaW5nX21lZGlhbl9hZ2VxFFgLAAAAdG90YWxfcm9vbXNxFVgOAAAAdG90YWxfYmVkcm9vbXNxFlgKAAAAcG9wdWxhdGlvbnEXWAoAAABob3VzZWhvbGRzcRhYDQAAAG1lZGlhbl9pbmNvbWVxGVgPAAAAb2NlYW5fcHJveGltaXR5cRpldHEbYi6VLgEAAAAAAACMDm5fZmVhdHVyZXNfaW5flEsJjAhfY29sdW1uc5RdlChoNmhWZYwdX3RyYW5zZm9ybWVyX3RvX2lucHV0X2luZGljZXOUfZQoaA9dlChLAEsBSwJLA0sESwVLBksH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
metadata:
  name: ml-models
```

Go to Topology from the Developer view and click on Add->Import from Git

1. Use this git repository URL: https://github.com/atarazana/ml-bk.git
2. Edit Import Strategy and choose `Dockerfile`, type in *Containerfile* into `Dockerfile path`
3. Application name should be: *ml-app*
4. Name *ml-bk*

Click on `Deployment` and add this environment variable:

```sh
MODEL_PATH => "/models/model.joblib"
```

Click on `Create`.

Then edit deployment and add <1> and <2>:

```yaml
    spec:
      containers:
      - env:
        - name: MODEL_PATH
          value: "/models/model.joblib"
        ...
        imagePullPolicy: Always
        volumeMounts: # <1>
        - mountPath: /models
          name: ml-models-volume
      ...
      schedulerName: default-scheduler
      volumes: # <2>
      - name: ml-models-volume
        secret:
          defaultMode: 420
          secretName: ml-models
```

<1> Mount point to read joblib from
<2> Volume definition from secret

# Manually deploying ml-ui

## Adding Node JS 18 Image Stream if needed

```sh
kubectl patch is nodejs -n openshift --type='json' -p='[{"op": "add", "path": "/spec/tags/-", "value": {"name": "18-ubi8", "annotations": {"description": "Build and run Node.js 18 applications on UBI 8. For more information about using this builder image, including OpenShift considerations, see https://github.com/sclorg/s2i-nodejs-container/blob/master/18-minimal/README.md.", "iconClass": "icon-nodejs", "openshift.io/display-name": "Node.js 18 (UBI 8)", "openshift.io/provider-display-name": "Red Hat, Inc.", "sampleRepo": "https://github.com/sclorg/nodejs-ex.git", "tags": "builder,nodejs", "version": "18"}, "from": {"kind": "DockerImage", "name": "registry.access.redhat.com/ubi8/nodejs-18:1-71.1698060565"}, "generation": 4, "importPolicy": {"importMode": "Legacy"}, "referencePolicy": {"type": "Source"}}}]'
```

Go to Topology from the Developer view and click on Add->Import from Git

1. Use this git repository URL: https://github.com/atarazana/ml-ui.git
2. Edit Import Strategy and choose `Dockerfile`, type in *Containerfile* into `Dockerfile path`
3. Application name should be: *ml-app*
4. Name *ml-bk*

Click on `Deployment` and add this environment variable:

```sh
MODEL_PATH => "/models/model.joblib"
```

Click on `Create`.

Deploy from git using s2i wizzard. Add this environment variable:

```sh
BACKEND_URL => "http://ml-bk:8080"
```
