# SVT demo — post one engagement event to Data Cloud Ingestion API
# Usage: fill in $clientId, $clientSecret, and $ingestUrl, then run in PowerShell

param(
    [string]$EventId = "LEAD-EVT-9003",
    [string]$ProspectId = "LEAD-2002"
)

$clientId     = "PASTE_CONSUMER_KEY"
$clientSecret = "PASTE_CONSUMER_SECRET"
$instanceUrl  = "https://orgfarm-6f6cec7b7b-dev-ed.develop.my.salesforce.com"

# Full URL from Setup → Ingestion API → Share Developer Information
# Must include /api/v1/ingest/sources/.../engagement_event (not hostname only)
$ingestUrl    = "https://YOUR-TENANT.c360a.salesforce.com/api/v1/ingest/sources/SVT_Engagement_Events/engagement_event"

Write-Host "--- Step 1: Salesforce token ---"
$step1 = Invoke-RestMethod -Method Post -Uri "$instanceUrl/services/oauth2/token" -Body @{
    grant_type    = "client_credentials"
    client_id     = $clientId
    client_secret = $clientSecret
} -ContentType "application/x-www-form-urlencoded"
Write-Host "Step 1 OK. Scopes: $($step1.scope)"

Write-Host "--- Step 2: Data Cloud token ---"
$step2 = Invoke-RestMethod -Method Post -Uri "$instanceUrl/services/a360/token" -Body @{
    grant_type         = "urn:salesforce:grant-type:external:cdp"
    subject_token      = $step1.access_token
    subject_token_type = "urn:ietf:params:oauth:token-type:access_token"
} -ContentType "application/x-www-form-urlencoded"
Write-Host "Step 2 OK"

Write-Host "--- Step 3: Ingest event ---"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
$body = @"
{"data":[{"event_id":"$EventId","prospect_id":"$ProspectId","event_type":"TestRideRequested","event_timestamp":"$timestamp","model":"SVT Stride 200 Demo","channel":"Web"}]}
"@

try {
    $response = Invoke-WebRequest -Method Post -Uri $ingestUrl `
        -Headers @{ Authorization = "Bearer $($step2.access_token)" } `
        -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "STATUS:" $response.StatusCode
    Write-Host "BODY:" $response.Content
    Write-Host "Wait 3-5 minutes, then check Data Explorer → Website Engagement"
} catch {
    Write-Host "ERROR STATUS:" $_.Exception.Response.StatusCode.value__
    $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
    Write-Host "ERROR BODY:" $reader.ReadToEnd()
}
