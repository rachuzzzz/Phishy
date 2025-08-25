# PowerShell script to update .env with ngrok URL
param(
    [Parameter(Mandatory=$true)]
    [string]$NgrokUrl
)

$envFile = "C:\Users\thoma\desktop\phishy\.env"

Write-Host "Updating .env with ngrok URL: $NgrokUrl" -ForegroundColor Green

# Read the .env file
$content = Get-Content $envFile

# Update the BASE_URL line
$updatedContent = $content | ForEach-Object {
    if ($_ -match "^BASE_URL=") {
        "BASE_URL=$NgrokUrl"
    } else {
        $_
    }
}

# Write back to .env file
$updatedContent | Set-Content $envFile

Write-Host "✅ .env file updated successfully!" -ForegroundColor Green
Write-Host "Please restart your Phishy backend server for changes to take effect." -ForegroundColor Yellow

# Show the updated content
Write-Host "`nUpdated .env content:" -ForegroundColor Cyan
Get-Content $envFile