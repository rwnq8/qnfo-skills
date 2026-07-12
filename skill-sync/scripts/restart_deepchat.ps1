# Restart DeepChat - kill all existing processes and launch fresh
# Used after skill sync to reload all skills

$ErrorActionPreference = "Stop"

Write-Host "Restarting DeepChat..." -ForegroundColor Cyan

# Find and kill all DeepChat processes
$processes = Get-Process -Name "DeepChat*" -ErrorAction SilentlyContinue
if ($processes) {
    Write-Host "Killing $($processes.Count) DeepChat process(es)..." -ForegroundColor Yellow
    $processes | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Find DeepChat executable
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\DeepChat\DeepChat.exe",
    "$env:PROGRAMFILES\DeepChat\DeepChat.exe",
    "${env:ProgramFiles(x86)}\DeepChat\DeepChat.exe"
)

$deepchatPath = $null
foreach ($p in $possiblePaths) {
    if (Test-Path $p) {
        $deepchatPath = $p
        break
    }
}

if ($deepchatPath) {
    Write-Host "Launching: $deepchatPath" -ForegroundColor Green
    Start-Process -FilePath $deepchatPath
    Write-Host "DeepChat restarted successfully." -ForegroundColor Green
} else {
    Write-Host "ERROR: DeepChat executable not found at:" -ForegroundColor Red
    foreach ($p in $possiblePaths) {
        Write-Host "  $p" -ForegroundColor Red
    }
    exit 1
}
