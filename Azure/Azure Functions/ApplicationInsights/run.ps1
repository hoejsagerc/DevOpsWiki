using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata)


$client = [Microsoft.ApplicationInsights.TelemetryClient]::new()
$client.InstrumentationKey = '61f2a6c0-2f27-4094-9a2a-c60933a832b6'
$client.Context.User.Id = $env:UserName
$client.Context.Session.Id = $PID


# Sending a Track Trace message
[Microsoft.ApplicationInsights.DataContracts.SeverityLevel]::Information # Information, Critical, Error, Warning, Verbose
$client.TrackTrace("Hello, World", "Information")
# Message can be force sent
$client.Flush() # If not used then the message will be queued


# Sending a Metric Message
$client.TrackMetric("Metric", (Get-Random))
$client.Flush()


# Metric with Properties
$dct = [System.Collections.Generic.Dictionary[string, string]]::new()
$dct.Add("LANG", $env:LANG)
$client.Flush()

$client.TrackMetric("Metric", (Get-Random), $dct)
$client.Flush()


# You can also track Pageviews or "Script runs"
$client.TrackPageView($MyInvocation.MyCommand.Name)
$client.Flush()


# You can also track Exceptions <-- Exceptions can be found in the failures tab
# If you give an exception type they will be sorted
$client.TrackException([System.Exception]::new("Hello"))
$client.Flush()

# Another example of an exception
try {
    Write-Host "Hello World"
}
catch {
    $client.TrackException($_)
    $client.Flush()    
}



# Here is a small function for passing a request
# This function could be used for meassuring the performance of your code
Function Measure-AICommand {
    Param(
        $name,
        $ScriptBlock
    )
    $sw = [System.Diagnostics.Stopwatch]::new()
    $sw.start()

    $status = "OK"
    try {
        & $ScriptBlock
    }
    catch {
        $status = $_.ToString();
    }

    $client.TrackRequest($name, (Get-Date),  $sw.Elapsed, $status, $status -eq "OK")
    $client.Flush()

    $sw.Stop()
}

Measure-AICommand -ScriptBlock {j
    Start-Sleep (Get-Random -min 1 -max 5)
} -Name 'Sleeping'



# You can track dependencies <-- If your script is connecting to an Api for example
Function Test-Url {
    param (
        $url
    )
    $sw = [System.Diagnostics.Stopwatch]::new()
    $sw.Start()

    $status = $true
    try {
        Invoke-Webrequest -Uri $Url
    }
    catch {
        $status = $false
    }

    $client.TrackDependency("HTTP", $Url, "", (Get-Date), $sw.Elapsed, $Status)
    $client.Flush()

    $sw.stop()
}

Test-Url -Url 'https://www.google123.com' # <-- will fail


# Write to the Azure Functions log stream.
Write-Host "PowerShell HTTP trigger function processed a request."

# Interact with query parameters or the body of the request.
$name = $Request.Query.Name
if (-not $name) {
    $name = $Request.Body.Name
}

$body = "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."

if ($name) {
    $body = "Hello, $name. This HTTP triggered function executed successfully."
}

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $body
})
