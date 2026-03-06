# Test the SHL Recommender API

Write-Host "`n=== Testing SHL Recommender API ===" -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Health: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ API not running. Start it with: uvicorn api.main:app --reload" -ForegroundColor Red
    exit
}

# Test 2: Get Recommendations
Write-Host "`n2. Testing Recommend Endpoint..." -ForegroundColor Yellow

$body = @{
    query = "Python developer with SQL skills"
    k = 10
    balanced = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "✅ Got $($response.recommended_assessments.Count) recommendations" -ForegroundColor Green
    Write-Host "`nTop 5 Results:" -ForegroundColor Cyan
    
    for ($i = 0; $i -lt [Math]::Min(5, $response.recommended_assessments.Count); $i++) {
        $assessment = $response.recommended_assessments[$i]
        Write-Host "  $($i+1). $($assessment.name)" -ForegroundColor White
        Write-Host "     Type: $($assessment.test_type -join ', ')" -ForegroundColor Gray
        Write-Host "     URL: $($assessment.url)" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Green
Write-Host ""
