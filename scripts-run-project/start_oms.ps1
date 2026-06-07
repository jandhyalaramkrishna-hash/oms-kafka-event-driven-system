Start-Process powershell -ArgumentList "cd app; python main.py"

Write-Host "🚀 OMS FULL CLEAN START"

# Always start from root
Set-Location $PSScriptRoot

# Stop everything
Write-Host "🛑 Stopping old services..."
docker-compose down -v

# Start Kafka + Zookeeper + Prometheus
Write-Host "🐳 Starting Docker services..."
docker-compose up -d

Start-Sleep -Seconds 10

# Start API
Write-Host "🌐 Starting API..."
Start-Process powershell -ArgumentList "cd app; python main.py"

# Start Consumer
Write-Host "📥 Starting Consumer..."
Start-Process powershell -ArgumentList "cd consumer; python consumer_worker.py"

# (Optional) Producer
Write-Host "📤 Starting Producer..."
Start-Process powershell -ArgumentList "cd producer; python producer.py"

# Open Swagger
Start-Process "http://localhost:8000/docs"

# Open Prometheus
Start-Process "http://localhost:9091"

Write-Host "✅ OMS Started Successfully"