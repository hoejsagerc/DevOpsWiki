# Running a Time triggered function in a Container image

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

> Timer trigger

> Function name: MyTimerFunction
```

</br>

## Changing the Timer

You will need to change the timer according to when and how often your function needs to run

Open the file /MyTimerFunction/function.json and change the property "schedule".

i will change the timer to "0/20 * * * * *" to make it run every 20 seconds.

You can follow the below basic examples:

| Expression | Description | Runs At |
| - | - | - |
| 0 * * * * * | every minute | 09:00:00; 09:01:00; 09:02:00; … 10:00:00 |
| 0 */5 * * * * | every 5 minutes | 09:00:00; 09:05:00 |
| 0 0 * * * * | every hour (hourly) | 09:00:00; 10:00:00; 11:00:00 | 
| 0 0 */6 * * * | every 6 hours | 06:00:00; 12:00:00; 18:00:00; 00:00:00 |
| 0 0 8-18 * * * | every hour between 8-18 | 08:00:00; 09:00:00; … 18:00:00; 08:00:00 | 
| 0 0 0 * * * | 0 0 0 * * * | Mar 1, 2017 00:00:00; Mar 2, 2017 00:00:00 | 
| 0 0 10 * * * | every day at 10:00:00 | Mar 1, 2017 10:00:00; Mar 2, 2017 10:00:00 |
| 0 0 * * * 1-5 | every hour on workdays | Mar 3 (FRI), 2017 22:00:00; Mar 3 (FRI), 2017 23:00:00; Mar 6 (MON), 2017 00:00:00 |
| 0 0 0 * * 0 | every sunday (weekly) | Mar 5 (SUN), 2017 00:00:00; Mar 12 (SUN), 2017 00:00:00 |
| 0 0 9 * * MON | every monday at 09:00:00 | Mar 6 (MON), 2017 09:00:00; Mar 13 (MON), 2017 09:00:00 |
| 0 0 0 1 * * | every 1st of month (monthly) | Mar 1, 2017 00:00:00; Apr 1, 2017 00:00:00; May 1, 2017 00:00:00 |
| 0 0 0 1 1 * | every 1st of january (yearly) | Jan 1, 2017 00:00:00; Jan 1, 2018 00:00:00; Jan 1, 2019 00:00:00 |
| 0 0 * * * SUN | every hour on sunday | Mar 5 (SUN), 2017 23:00:00; Mar 12 (SUN), 2017 00:00:00; Mar 12 (SUN), 2017 01:00:00 |
| 0 0 0 * * SAT,SUN | every saturday and sunday | Mar 3 (SUN), 2017 00:00:00; Mar 11 (SAT) 00:00:00; Mar 12 (SUN), 2017 00:00:00 |
| 0 0 0 * * 6,0 | every saturday and sunday | Mar 3 (SUN), 2017 00:00:00; Mar 11 (SAT) 00:00:00; Mar 12 (SUN), 2017 00:00:00 |
| 0 0 0 1-7 * SUN | every first sunday of the month at 00:00:00 | Mar 5 (SUN), 2017 00:00:00; Apr 2 (SUN), 2017 00:00:00 |
| 11 5 23 * * * | daily at 23:05:11 | Mar 1, 2017 23:05:11; Mar 2, 2017 23:05:11 |
| 30 5 /6 * * * | every 6 hours at 5 minutes and 30 seconds | 06:05:30; 12:05:30; 18:05:30; 00:05:30 |
| */15 * * * * * | every 15 seconds | 09:00:15; 09:00:30; … 09:03:30; 09:03:45; 09:04:00 |

[Table source: https://arminreiter.com/2017/02/azure-functions-time-trigger-cron-cheat-sheet/](https://arminreiter.com/2017/02/azure-functions-time-trigger-cron-cheat-sheet/)

</br>

## Adding docker support for the Function

Inside the Functions directory run the command

```powershell
func init --docker-only
```

## Building, Publishing and testing container image with Azure

Building image in Azure Container Registry

```powershell
az acr build --image myrepo/pstimerfunction:v1 --registry $acrName --file Dockerfile .
```

Testing image in Azure Container Registry

```powershell
az acr run --registry $acrName --cmd "$($acrName).azurecr.io/myrepo/pstimerfunction:v1" /dev/null
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
az container create --name pstimerfunction `
    --resource-group $rg `
    --image "$($acrName).azurecr.io/myrepo/pstimerfunction:v1" `
    --registry-username $acrName `
    --registry-password $password `
    --dns-name-label pshttpfunction `
    --ports 80
```

you can now check the container logs and watch that it will run every 20 seconds

```powershell
az container attach --resource-group $rg --name pstimerfunction
```

</br>