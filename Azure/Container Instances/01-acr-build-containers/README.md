# How to build and test containers in Azure

In this section i will walkthrough how you can build a container from a Dockerfile directly in Azure.
Then in azure run the container and test if it is working

</br>

## Prerequisites

- You will need the Azure CLI installed [Download here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- You will need an Azure subscription

</br>

## Looking at the Application

So in the repository i have a folder named "/app". In the folder you will find a basic Python application.
Basicly this application will expose a local json file as an API.

In the folder you will find a main.py file. This file is the application code. You will find a folder named "data" and inside a users.json file. This file will be used as the "database". And at last you will find a requirements.txt. This file is used to handle all the 
libraries needed for the application.

The application it self can be used for viewing all available users, create new users and delete users from the "database".

</br>

## Creating a resource group and Azure Container Registry

Create a resource group:

```powershell
$rg = "rg-demo-containers"
$location = "westeurope"

az group create --name $rg --location $location
```

Create container registry:

```powershell
$acrName = "mycrazycontainerdemo"

az acr create --resource-group $rg --name $acrName --sku Basic 
```

</br>


## Explaining the Dockerfile

When creating the Dockerfile i will be building from the base python image, with version 3.9

```docker
FROM python:3.9
```

I will then copy the requirements file to the image and install all the prerequisites

```docker
COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

Then i will copy the rest of the application code into the container image

```docker
COPY ./app /code/app
```

And at last i will execute the run command for running the python application

```docker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```


</br>


## Building the container image

I can now build the container image directly in the Azure container registry

```powershell
az acr build --image myrepo/pythonapp:v1 --registry $acrName --file Dockerfile .
```

You can view that the image was pushed to container registry

```powershell
az acr repository show --name $acrName --image myrepo/pythonapp:v1
```

</br>

## Testing if the image works

You can run container images deployed to Azure Container Registry, directly in the Contianer registry for testing

```powershell
az acr run --registry $acrName --cmd "$($acrName).azurecr.io/myrepo/pythonapp:v1" /dev/null
```

Here you should see the uvicorn webserver starting without errors.
You will not be able to browse your applicationæ

</br>

## Deploy your image to a Container Instance

You can quickly deploy your container to a container instance in azure to browse your application


Firstly you will need to update the container registry to enable admnin access and the you will need to retrieve the password

```powershell
az acr update --name $acrName --admin-enabled true

$password = az acr credential show --name $acrName --query "passwords[0].value"-o tsv
```

Then you can deploy a new container instance

```powershell
az container create --name pythonapp `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/pythonapp:v1" `
    --registry-username $acrName `
    --registry-password $password `
    --dns-name-label pythonapp `
    --ports 80
```

you can find the url to the container by running the command:

```powershell
az container show -g $rg --name pythonapp --query ipAddress.fqdn -o tsv
```

or you can run the following command to get a overview of the provisioning

```powershell
az container show -g $rg -n pythonapp --query "{URL:ipAddress.fqdn, ProvisionState:provisioningState}" -o table
```

you can attach to the log stream by running the command:
```powershell
az container attach -g $rg -n pythonapp
```

</br>


## Updateing the container image for the container instance

you can run the following commands to build and redeploy the new container image.
Notice i have changed the image tag to "v2"

```powershell
az acr build --image myrepo/pythonapp:v2 --registry $acrName --file Dockerfile .

az container create --name pythonapp `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/pythonapp:v2" `
    --registry-username $acrName `
    --registry-password $password `
    --dns-name-label pythonapp `
    --ports 80
```