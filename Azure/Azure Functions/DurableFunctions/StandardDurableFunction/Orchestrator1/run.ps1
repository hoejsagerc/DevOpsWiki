param($Context)


$Address = ($Context.Input | ConvertFrom-Json).Addresses



######### STANDARD METHOD ##########

# Invoking the Activity function in serial => 1 by 1
$allResults = New-Obejct System.Collections.ArrayList
foreach ($address in $Address) {
    $result = Invoke-DurableActivity -FunctionName 'Activity1' -Input $address
    $allResults.Add($result)
}
Write-Output $allResults
#>



######### FANOUT METHOD #########

<# Invoking the Activity function in parallel => all at once
$parallelTasks = foreach ($address in $Address) {
    Invoke-DurableActivity -FunctionName 'Activity1' -Input $address -NoWait
}

$results = Wait-ActivityFunction -Task $parallelTasks | Sort-Object -Property PortStatus, Address
return $results
#>

