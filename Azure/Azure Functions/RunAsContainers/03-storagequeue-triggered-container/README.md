# Running an Storage Queue triggered function in a Container image

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

Creating the Azure Storage Account

```powershell
$random = Get-Random
$storageName = "storage$($random)"

az storage account create `
  --name $storageName `
  --resource-group $rg `
  --kind StorageV2 `
  --location $location 
```

Storing the Connection String

```powershell
$connString = az storage account show-connection-string `
  -n $storageName `
  -g $rg `
  --query connectionString `
  -o tsv
```

Creating the Storage Queue

```powershell
az storage queue create --name myqueue --account-name $storageName
```

Test the queue by sending a message to the queue

```powershell
az storage message put `
  --queue-name myqueue `
  --content "Hello World" `
  --account-name $storageName `
  --connection-string $connString
```

Reading the message from the queue

```powershell
az storage message get `
  --queue-name myqueue `
  --account-name $storageName `
  --connection-string $connString
```
You should get an output from the message to send previos. This will also clear the queue.

</br>

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

> Azure Queue Storage trigger

> Function name: MyQueueFunction
```

</br>

## Changing function authLevel

You will need to change the function authentication level from "function" to "anonymouse" otherwise you will not be able to access the function when deployed as a container

open the file MyQueueFunction/function.json

Then change the property "queueName" to --> "myqueue"

And add *STORAGE_CONNECTION_STRING* to the "connection" property

The value _STORAGE_CONNECTIOn_STRING_ is the name of an environment variable we will provide to the container image when it is run. This could be changed to what ever you want just as long as you change the name for the environment variable when running the container image.

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
az acr build --image myrepo/psqueuefunction:v1 --registry $acrName --file Dockerfile .
```

Testing image in Azure Container Registry

```powershell
az acr run --registry $acrName --cmd "$($acrName).azurecr.io/myrepo/psqueuefunction:v1" /dev/null
``` 

By running in ACR you can only see logs to check if no error occured and that image started successfully

You will properbly get and error similar to: AzureWebJobsSTORAGE_CONNECTION_STRING does not exist.

This is because the environmment variable is not provided. Just ignore for now.

</br>

## Pushing image to Azure Container Instance for full test

Enable admin access on ACR, and retrieve the password

```powershell
az acr update --name $acrName --admin-enabled true

$password = az acr credential show --name $acrName --query "passwords[0].value"-o tsv
```

Push container image to Azure Container Instance

```powershell
az container create --name psqueuefunction `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/psqueuefunction:v1" `
    --registry-username $acrName `
    --registry-password $password `
    --environment-variables STORAGE_CONNECTION_STRING=$connString `
    --dns-name-label psqueuefunction `
    --ports 80
```

</br>

## Testing the function

Connect to the logs of the container

```powershell
az container attach --resource-group $rg --name psqueuefunction
```

then in another terminal run the following command to send a message to the queue:
Notice we need to Bas64 encode the message, otherwise the message will end up in a poisen queue.

```powershell
$Bytes = [System.Text.Encoding]::Unicode.GetBytes('Hello World')
$EncodedText =[Convert]::ToBase64String($Bytes)

az storage message put `
  --queue-name myqueue `
  --content $EncodedText `
  --account-name $storageName `
  --connection-string $connString
```

Then wait a few seconds you should now see in the logs that the message will get processed.

