# Batch trigger R2 migration - optimized for Worker CPU limits
$workerUrl = "https://papers-server.q08.workers.dev"
$batchSize = 20
$offset = 5  # First 5 already done
$maxBatches = 50
$batch = 0
$totalUploaded = 5

Write-Host "=== QNFO Paper R2 Migration (batchSize=$batchSize) ==="
Write-Host "Starting from offset=$offset"
Write-Host ""

do {
    $batch++
    Write-Host "--- Batch $batch (offset=$offset, size=$batchSize) ---"
    
    $body = @{ batchSize = $batchSize; offset = $offset } | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "$workerUrl/admin/migrate-r2" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
        
        $totalUploaded += $response.batch.uploaded
        Write-Host "  Uploaded: $($response.batch.uploaded) | Errors: $($response.batch.errors) | Total: $totalUploaded"
        Write-Host "  Progress: $($response.progress)"
        
        if ($response.errorDetails -and $response.errorDetails.Count -gt 0) {
            Write-Host "  ERRORS:"
            foreach ($e in $response.errorDetails) { Write-Host "    $($e.slug): $($e.error)" }
        }
        
        $offset = $response.nextOffset
        $hasMore = $response.hasMore
        
        if ($hasMore) { Start-Sleep -Seconds 2 }
    } catch {
        Write-Host "  ERROR (batch may have been too large, trying smaller): $_"
        # Retry with smaller batch
        $smallBody = @{ batchSize = 10; offset = $offset } | ConvertTo-Json
        try {
            $response = Invoke-RestMethod -Uri "$workerUrl/admin/migrate-r2" -Method POST -Body $smallBody -ContentType "application/json" -TimeoutSec 30
            $totalUploaded += $response.batch.uploaded
            Write-Host "  Retry ok: Uploaded $($response.batch.uploaded)"
            $offset = $response.nextOffset
            $hasMore = $response.hasMore
        } catch {
            Write-Host "  Retry also failed. Stopping."
            break
        }
    }
    
    Write-Host ""
} while ($hasMore -and $batch -lt $maxBatches)

Write-Host "=== Migration Complete ==="
Write-Host "Total uploaded: $totalUploaded"
Write-Host "Batches run: $batch"
