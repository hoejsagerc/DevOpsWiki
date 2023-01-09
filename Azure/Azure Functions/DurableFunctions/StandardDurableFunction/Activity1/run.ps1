param($Address)

Start-Sleep -Seconds 5

try {
    $pageStatus =  $((Invoke-WebRequest -Uri $Address).StatusCode)
}
catch {
    $portStatus = $null
}

$returnObject = [pscustomobject]@{
    Address = $Address
    StatusCode = $portStatus
}

return $returnObject