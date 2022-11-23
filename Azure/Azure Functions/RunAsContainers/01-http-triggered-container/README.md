# Running an Http triggered function in a Container image

In this guide i will walk throguh how you can create and package a PowerShell Azure Function
in a Container image and run the image on Azure Container Instance. This will not require you
to have Docker installed. Only Azure CLI and Function Core Tools is needed.

</br>

## Prerequisites

- Azure CLI Installed [Get it here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- An Azure Subscription
- Azure Function Core Tools v4 [Get it here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash)
  - You can find the installation guide under the heading: **Install the Azure Function Core Tools**

</br>

## Creating the Azure Environment

Create new resource group

```powershell
$rg = "rg-demo-functions"
$location = "westeurope"

az group create --name $rg --location $location
```

Creating the azure container registry

```powershell
$acrName = "mycrazycontainerdemo"

az acr create --resource-group $rg --name $acrName --sku Basic
```


## Creating the function

Once you have Azure Function Core tools installed you can create a new function from you PowerShell Terminal

```powershell
mkdir Functions

cd Functions

func new
```

Once you enter "func new" then you will be prompted for information when setting up the functions

select the following for an HTTP triggered PowerShell function

```powershell
> powershell

> HTTP trigger

> Function name: MyHttpFunction
```

</br>

## Changing function authLevel

You will need to change the function authentication level from "function" to "anonymouse" otherwise you will not be able to access the function when deployed as a container

open the file MyHttpFunction/function.json

then change the property "authLevel" from "function" --> "anonymous"

</br>

## Adding docker support for the Function

Inside the Functions directory run the command

```powershell
func init --docker-only
```

</br>

## Building, Publishing and testing container image with Azure

Building image in Azure Container Registry

```powershell
az acr build --image myrepo/pshttpfunction:v1 --registry $acrName --file Dockerfile .
```

Testing image in Azure Container Registry

```powershell
az acr run --registry $acrName --cmd "$($acrName).azurecr.io/myrepo/pshttpfunction:v1" /dev/null
``` 

By running in ACR you can only see logs to check if no error occured and that image started successfully


</br>

## Pushing image to Azure Container Instance for full test

Enable admin access on ACR, and retrieve the password

```powershell
az acr update --name $acrName --admin-enabled true

$password = az acr credential show --name $acrName --query "passwords[0].value"-o tsv
```

Push container image to Azure Container Instance

```powershell
az container create --name pshttpfunction `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/pshttpfunction:v1" `
    --registry-username $acrName `
    --registry-password $password `
    --dns-name-label pshttpfunction `
    --ports 80
```

</br>

## Testing the function

Find the url for the function 

```powershell
az container show -g $rg --name pshttpfunction --query ipAddress.fqdn
```

Check the container logs

```powershell
az container attach --resource-group $rg --name pshttpfunction
```

run the command:

```powershell
$name = "ScriptingChris"
(Invoke-WebRequest -uri "http://pshttpfunction.westeurope.azurecontainer.io/api/MyHttpFunction?name=$($name)").Content
```