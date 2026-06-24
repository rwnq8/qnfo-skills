# restart_deepchat.ps1 - KILL + RELAUNCH DeepChat (detached scheduler strategy)
# Usage: powershell -ExecutionPolicy Bypass -File restart_deepchat.ps1
$ErrorActionPreference = 'Stop'

$EXE = "$env:LOCALAPPDATA\Programs\DeepChat\DeepChat.exe"
if (-not (Test-Path $EXE)) {
    Write-Host 'FATAL: DeepChat.exe not found' -ForegroundColor Red
    exit 1
}

Write-Host 'RESTART: Detached scheduler strategy (kill-then-relaunch)' -ForegroundColor Cyan

$tmpScript = "$env:TEMP\deepchat_restart_scheduler.ps1"
$schedulerContent = @"
Start-Sleep -Seconds 3
Write-Host 'SCHEDULER: Killing all DeepChat processes...'
Get-Process -Name 'DeepChat' -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host 'SCHEDULER: Launching new DeepChat instance...'
Start-Process -FilePath '$EXE'
Write-Host 'SCHEDULER: Done. New DeepChat launched.'
"@

try {
    Set-Content -Path $tmpScript -Value $schedulerContent -Encoding UTF8 -ErrorAction Stop
} catch {
    Write-Host "FATAL: Failed to write scheduler: $_" -ForegroundColor Red
    exit 2
}

try {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'powershell.exe'
    $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$tmpScript`""
    $psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
    $psi.UseShellExecute = $true
    [System.Diagnostics.Process]::Start($psi) | Out-Null
    Write-Host 'RESTART: Detached scheduler started. DeepChat restarts in ~4s.' -ForegroundColor Green
    Write-Host 'RESTART: Conversation will terminate when old processes are killed.' -ForegroundColor Yellow
} catch {
    Write-Host "FATAL: Failed to launch scheduler: $_" -ForegroundColor Red
    exit 3
}

exit 0
