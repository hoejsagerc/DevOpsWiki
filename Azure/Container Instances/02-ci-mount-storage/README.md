# Mounting storage to an Azure Container Instance

**_This guide is a follow up to the folder "../01-acr-build-containers"_**

I assume you have a container instance already running in Azure

</br>

## Creating a storage account

You will need a storage account with azure files enabled, to mount the fileshare
to the container instance.

```powershell
$rg = "rg-demo-containers"
$location = "westeurope"
$storageName = "mycrazydemostorage"

az storage account create `
    --resource-group $rg `
    --name $storageName `
    --location $location `
    --sku Standard_LRS
```

</br>

## Creating the file share

```powershell
az storage share create `
    --name "containershare" `
    --account-name $storageName
```

</br>

## Retrieving the storage key

```powershell
$key = az storage account keys list -g $rg --account-name $storageName --query "[0].value" --output tsv
```

</br>

## Mounting the fileshare to the container instance

i will now mount the fileshare into the path /code/app/data/ inside the container

```powershell
$acrName = "mycrazycontainerdemo"

az container create --name pythonapp `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/pythonapp:v2" `
    --registry-username $acrName `
    --registry-password $password `
    --dns-name-label pythonapp `
    --ports 80 `
    --azure-file-volume-account-name $storageName `
    --azure-file-volume-account-key $key `
    --azure-file-volume-share-name "containershare" `
    --azure-file-volume-mount-path /code/app/data/
```

</br>

## recreating the files on the fileshare

Since the file share mount is empty the users.json file will now not be available in the application.
You can navigate to in the azure portal, to storage browser and then the file share.

You can now copy the users.json file to the containershare.

Now to check that the file is available inside the container you can exec directly into the container with the command:

```powershell
az container exec -g $rg -n pythonapp --exec-command "/bin/bash"

ls /code/app/data
```

you should now see the file. And if you run the the application it should work.

You should also be able to create a new user. Then restart the application and the user should stille be available.


</br>