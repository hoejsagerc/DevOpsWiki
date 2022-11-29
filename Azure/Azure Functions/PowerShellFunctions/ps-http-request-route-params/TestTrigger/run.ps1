using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata)


$people = @(
    @{Name="John"; Age=42},
    @{Name="Jane"; Age=36},
    @{Name="Bob"; Age=51}
)
# Write to the Azure Functions log stream.
Write-Host "PowerShell HTTP trigger function processed a request."

# Interact with query parameters or the body of the request.
$name = $Request.Params.Name
Write-Host $Name

if ($name -in $people.Name) {
    $output = $people | Where-Object {$_.Name -eq $name}
}
else {
    Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
        StatusCode = [HttpStatusCode]::NotFound
        Body = "Person not found"
    })
}

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $output
})
