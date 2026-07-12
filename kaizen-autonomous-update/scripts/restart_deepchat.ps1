# DeepChat Restart Script
# Kills all DeepChat processes and launches a fresh instance
# Usage: powershell -ExecutionPolicy Bypass -File restart_deepchat.ps1

Write-Host "[KAIZEN] Restarting DeepChat..." -ForegroundColor Cyan

# Kill all DeepChat processes
$deepchatProcs = Get-Process -Name "DeepChat*" -ErrorAction SilentlyContinue
if ($deepchatProcs) {
    Write-Host "  Killing $($deepchatProcs.Count) DeepChat process(es)..." -ForegroundColor Yellow
    $deepchatProcs | Stop-Process -Force
    Start-Sleep -Milliseconds 2000
    Write-Host "  Processes killed." -ForegroundColor Green
} else {
    Write-Host "  No DeepChat processes found." -ForegroundColor Gray
}

# Launch fresh DeepChat instance
$deepchatPath = "$env:LOCALAPPDATA\Programs\DeepChat\DeepChat.exe"
if (Test-Path $deepchatPath) {
    Write-Host "  Launching DeepChat..." -ForegroundColor Cyan
    Start-Process $deepchatPath
    Write-Host "  DeepChat launched. Skills v4.0 and v3.2 will load." -ForegroundColor Green
} else {
    Write-Host "  DeepChat.exe not found at $deepchatPath" -ForegroundColor Red
    Write-Host "  Please launch DeepChat manually from the Start Menu." -ForegroundColor Yellow
}

# Post-restart verification hint
Write-Host ""
Write-Host "[KAIZEN] After restart, verify skills loaded:" -ForegroundColor Cyan
Write-Host "  powershell -File %USERPROFILE%\.deepchat\verify_skills.ps1" -ForegroundColor Gray
