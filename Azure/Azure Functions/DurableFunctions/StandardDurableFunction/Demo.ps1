<#

    APPSETTING TO APPLY IN THE AZURE FUNCTION APP

    (can be tuned to your needs)
    FUNCTIONS_WORKER_PROCESS_COUNT: 10
    PSWorkerInProcConcurrencyUpperBound: 10   <--- Specific to PowerShell

#>




$uri = "http://localhost:7071/api/orchestrators/Orchestrator1"

$addressList = @(
    "1.1.1.1", 
    "1.0.0.1", 
    "google.com", 
    "8.8.8.8", 
    "8.8.4.4", 
    "scriptingchris.tech"
)


$body = @{addresses = $addressList} | ConvertTo-Json


$response = Invoke-RestMethod -Uri $uri -Method POST -Body $body -ContentType "application/json"

$status = "Running"
while (($status -eq "Running") -or ($status -eq "Pending")) {
    Start-Sleep -Seconds 5
    $query = Invoke-RestMethod -Uri $response.statusQueryGetUri -Method GET
    $status = $query.runtimeStatus
    $status
}

Write-Output "- Runtime: $((New-TimeSpan -Start $query.createdTime -End $query.lastUpdatedTime).TotalSeconds) Seconds"