Write-Host "==============================="
Write-Host "OMS FULL CLEAN START"
Write-Host "==============================="

Set-Location "C:\oms-kafka-event-driven-system"

# 🔴 STEP 1: Kill old Python processes (API + Consumer)
Write-Host "Cleaning old Python processes..."
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# 🔴 STEP 2: Free port 8000 if stuck
Write-Host "Freeing port 8000..."
$port = 8000
$proc = netstat -ano | findstr :$port
if ($proc) {
    $pid = ($proc -split "\s+")[-1]
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
}

# 🔴 STEP 3: Clean Docker COMPLETELY
Write-Host "Cleaning Docker..."
docker compose down -v
docker system prune -f

# 🔴 STEP 4: Start fresh containers
Write-Host "Starting Docker containers..."
docker compose up -d

# 🔴 STEP 5: Wait for Kafka properly
Write-Host "Waiting for Kafka..."
while ($true) {
    docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list *> $null
    if ($LASTEXITCODE -eq 0) { break }
    Write-Host "Kafka not ready... retrying in 5 sec"
    Start-Sleep -Seconds 5
}

Write-Host "Kafka Ready!"

# 🔴 STEP 6: Create topics
Write-Host "Creating topics..."
docker exec kafka kafka-topics --create --if-not-exists --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec kafka kafka-topics --create --if-not-exists --topic orders_dlq --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# 🔴 STEP 7: Start API
Write-Host "Starting API..."
Start-Process powershell -ArgumentList "cd C:\oms-kafka-event-driven-system; python -m uvicorn app.main:app --reload"

Start-Sleep -Seconds 8

# 🔴 STEP 8: Start Consumer
Write-Host "Starting Consumer..."
Start-Process powershell -ArgumentList "cd C:\oms-kafka-event-driven-system; python consumer_worker.py"

Start-Sleep -Seconds 5

# 🔴 STEP 9: Start DLQ Monitor
Write-Host "Starting DLQ Monitor..."
Start-Process powershell -ArgumentList "docker exec -it kafka kafka-console-consumer --topic orders_dlq --from-beginning --bootstrap-server localhost:9092"

Start-Sleep -Seconds 5

# 🔴 STEP 10: Run Newman WITH REPORTS
Write-Host "Running Newman Tests..."
newman run OMS-postman_collection.json `
  -e OMS-postman_environment.json `
  -d OMS_CLEAN_1000_RECORDS.csv `
  --reporters cli `
  --reporter-cli-no-success-assertions

Write-Host "==============================="
Write-Host "OMS FULL FLOW COMPLETED"
Write-Host "==============================="