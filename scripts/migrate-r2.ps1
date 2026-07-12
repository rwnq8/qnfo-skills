# Batch trigger R2 migration for all 616 papers
$workerUrl = "https://papers-server.q08.workers.dev"
$batchSize = 50
$offset = 0
$maxBatches = 20
$batch = 0

Write-Host "=== QNFO Paper R2 Migration ==="
Write-Host "Worker: $workerUrl"
Write-Host "Batch size: $batchSize"
Write-Host ""

do {
    $batch++
    Write-Host "--- Batch $batch (offset=$offset, size=$batchSize) ---"
    
    $body = @{ batchSize = $batchSize; offset = $offset } | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri "$workerUrl/admin/migrate-r2" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
        Write-Host "  Status: $($response.status)"
        Write-Host "  Uploaded: $($response.batch.uploaded) | Errors: $($response.batch.errors)"
        Write-Host "  Progress: $($response.progress)"
        Write-Host "  HasMore: $($response.hasMore)"
        
        if ($response.successDetails -and $response.successDetails.Count -gt 0) {
            Write-Host "  Sample uploads:"
            foreach ($d in $response.successDetails) {
                Write-Host "    $($d.slug) → $($d.r2Path) ($($d.source))"
            }
        }
        
        if ($response.errorDetails -and $response.errorDetails.Count -gt 0) {
            Write-Host "  Errors:"
            foreach ($e in $response.errorDetails) {
                Write-Host "    $($e.slug): $($e.error)"
            }
        }
        
        $offset = $response.nextOffset
        $hasMore = $response.hasMore
        
        if ($hasMore) {
            Write-Host "  Pausing 3s before next batch..."
            Start-Sleep -Seconds 3
        }
    } catch {
        Write-Host "  ERROR: $_"
        break
    }
    
    Write-Host ""
} while ($hasMore -and $batch -lt $maxBatches)

Write-Host "=== Migration Complete ==="
Write-Host "Total batches: $batch"
