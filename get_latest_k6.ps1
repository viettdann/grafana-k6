# Fetch the latest release information
$LatestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/grafana/k6/releases/latest"

# Extract the tag name (version)
$Version = $LatestRelease.tag_name

# Construct the filename
$Filename = "k6-$Version-windows-amd64.zip"

# Extract the download URL for the appropriate file
$DownloadUrl = ($LatestRelease.assets | Where-Object { $_.name -eq $Filename }).browser_download_url

if (-not $DownloadUrl) {
    Write-Host "Could not find download URL for $Filename"
    exit 1
}

# Create bin directory if it doesn't exist
New-Item -ItemType Directory -Force -Path .\bin | Out-Null

# Download the file
Write-Host "Downloading $Filename..."
Invoke-WebRequest -Uri $DownloadUrl -OutFile $Filename

Write-Host "Download complete: $Filename"

# Extract the binary
Write-Host "Extracting k6 binary..."
$TempDir = ".\temp_extract"
Expand-Archive -Path $Filename -DestinationPath $TempDir -Force

# Find and move the k6.exe file
$K6Exe = Get-ChildItem -Path $TempDir -Recurse -Filter "k6.exe" | Select-Object -First 1
if ($K6Exe) {
    Move-Item -Path $K6Exe.FullName -Destination ".\bin\k6.exe" -Force
    Write-Host "k6 binary installed to .\bin\k6.exe"
} else {
    Write-Host "Error: k6.exe not found in the extracted files"
    exit 1
}

# Clean up
Remove-Item -Path $Filename -Force
Remove-Item -Path $TempDir -Recurse -Force

# Verify installation
if (Test-Path ".\bin\k6.exe") {
    Write-Host "k6 binary successfully installed to .\bin\k6.exe"
} else {
    Write-Host "Error: Failed to install k6 binary"
    exit 1
}