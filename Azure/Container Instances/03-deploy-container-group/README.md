# How to deploy an Azure Container Group

[Microsoft Docs](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-container-groups)


In this guide i will deploy two micro services in a group deployment to Azure Container Instance.

</br>

## Prerequisites

I assume you have a container instance already running in Azure and that you have read guide 01 and 02 in 'Container Instances'


</br>>


## Folder structure

```plaintext
│   deploy-aci.yaml
│   README.md
│
└───Services
    ├───api
    │   │   Dockerfile
    │   │   requirements.txt
    │   │
    │   └───app
    │       │   main.py
    │       │
    │       ├───data
    │       │       users.json
    │       │
    │       └───__pycache__
    │               main.cpython-39.pyc
    │
    └───app
        │   Dockerfile
        │   requirements.txt
        │
        └───app
            │   main.py
            │
            └───templates
                    index.html
```

*deploy-aci.yaml* => ACI container group deployment manifest
*api*=> All files relevant to the api micro service
*app* => All files relevant to the webapp micro service

</br>

## Building and pushing the images

start by building and testing the webapp container image

```powershell
$acrName = "mycrazycontainerdemo"

cd Services/app

az acr build --image myrepo/webapp:v1 --registry $acrName --file Dockerfile .

az acr run --registry $acrName --cmd "mycrazycontainerdemo.azurecr.io/myrepo/webapp:v1" /dev/null
```

then build and test the api container image

```powershell
cd Services/api

az acr build --image myrepo/api:v1 --registry $acrName --file Dockerfile .

az acr run --registry $acrName --cmd "mycrazycontainerdemo.azurecr.io/myrepo/api:v1" /dev/null
```

</br>

## Creating the deployment yaml file


Defining the metadata for the container instance
```yaml
apiVersion: 2019-12-01
location: westeurope
name: myMicroService
```

then set the properties for the instance. Here i start wit the containers.
The first container:

```yaml
containers:
- name: webapp
    properties:
        image: mycrazycontainerdemo.azurecr.io/myrepo/webapp:v1
        resources:
        requests:
            cpu: 1
            memoryInGb: 1.5
        ports:
        - port: 80
```

then for the second container

```yaml
- name: api
    properties:
        image: mycrazycontainerdemo.azurecr.io/myrepo/api:v1
        resources:
        requests:
            cpu: 1
            memoryInGb: 1.5
        ports:
        - port: 5001
```

I am setting the OS to Linux

```yaml
osType: Linux
```

Then i define an ip address and adding a dns label to the container instance

```yaml
ipAddress:
    type: Public
    ports:
    - protocol: tcp
        port: 80
    dnsNameLabel: myMicroService
```

I then add the credentials for my Azure Container Registry (don't worry the key is no longer valid.)

```yaml
imageRegistryCredentials:
    - server: mycrazycontainerdemo.azurecr.io
    username: mycrazycontainerdemo
    password: 3ftll=u0yRbCOGKfLERp4n9WnXQ1C1k7
```

at last i will set some more meta data

```yaml
tags: {exampleTag: tutorial}
type: Microsoft.ContainerInstance/containerGroups
```

All yaml properties can be found here: [Yaml schema](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-reference-yaml)

</br>


## Deploying the Container Group Instance

Deploying the containers

```powershell
az container create --resource-group $rg --file .\deploy-aci.yaml
```

you can stream the logs for the individual container by defining the name of the container

```powershell
az container attach -g $rg -n myMicroService --container-name webapp
```