$workerUrl = "https://papers-server.q08.workers.dev"
$batchSize = 25
$offset = 48
$totalUploaded = 48
$batch = 0
$maxBatches = 30

while ($batch -lt $maxBatches) {
    $batch++
    $body = "{`"batchSize`":$batchSize,`"offset`":$offset}"
    
    try {
        $r = Invoke-RestMethod -Uri "$workerUrl/admin/migrate-r2" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
        $totalUploaded += $r.batch.uploaded
        Write-Host "Batch $batch offset=$offset uploaded=$($r.batch.uploaded) errors=$($r.batch.errors) total=$totalUploaded $($r.progress)"
        $offset = $r.nextOffset
        
        if (-not $r.hasMore) {
            Write-Host "All papers processed!"
            break
        }
        
        Start-Sleep -Seconds 2
    }
    catch {
        Write-Host "ERROR at offset=$offset batchSize=$batchSize : $_"
        if ($batchSize -gt 5) {
            $batchSize = [Math]::Floor($batchSize / 2)
            Write-Host "Reducing batchSize to $batchSize and retrying..."
        }
        else {
            Write-Host "Stopping after repeated failures."
            break
        }
    }
}

Write-Host "=== Complete: $totalUploaded papers uploaded ==="
