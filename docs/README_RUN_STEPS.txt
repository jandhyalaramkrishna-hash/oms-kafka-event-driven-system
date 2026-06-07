OMS EVENT-DRIVEN SYSTEM — ONE CLICK EXECUTION (FINAL)
cd scripts-run-project
.\start_oms.ps1

STEP 0 — CLEAN EVERYTHING (MANDATORY)
# Stop all Python processes
taskkill /F /IM python.exe

# Stop all Docker containers
docker ps -aq | ForEach-Object { docker stop $_ }
docker ps -aq | ForEach-Object { docker rm $_ }
# Remove all containers
docker rm $(docker ps -aq)

# Clean Docker system
docker system prune -f

# Free port 8000 (API)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
================
STEP 1 — START DOCKER (Kafka + Zookeeper + Prometheus)
cd C:\oms-kafka-event-driven-system
docker compose up -d

Verify:
docker ps 

You must see:

kafka
zookeeper
prometheus
================
STEP 2 — START API (FASTAPI PRODUCER)
cd C:\oms-kafka-event-driven-system
python -m uvicorn app.main:app --reload

Open Swagger
http://localhost:8000/docs

================
STEP 3 — START CONSUMER (DLQ + RETRY)
cd consumer
python consumer_worker.py
================
STEP 4 — VERIFY API (POSTMAN / SWAGGER)
post at url
http://localhost:8000/orders
================
STEP 5 — RUN NEWMAN (1000 RECORDS TEST)
# ONE TIME INSTALLATION
npm install -g newman
npm install -g newman-reporter-html newman-reporter-json
npm install -g allure-commandline

---------------------------------------------------------------------------------------

cd C:\oms-kafka-event-driven-system

newman run OMS-postman_collection.json `
-e OMS-postman_environment.json `
-d testdata\OMS_CLEAN_1000_RECORDS.csv `
-r cli,html,json `
--reporter-html-export newman\report.html `
--reporter-json-export newman\report.json
=================
STEP 6 — ALLURE REPORT (ADVANCED)
allure generate newman\allure-results --clean -o newman\allure-report
allure open newman\allure-report
================
STEP 7 — CHECK DLQ (Kafka Console)
docker exec -it kafka kafka-console-consumer `
--topic orders_dlq `
--from-beginning `
--bootstrap-server localhost:9092
================
STEP 8 — PROMETHEUS (METRICS)
monitoring/prometheus/
prometheus.exe --config.file=prometheus.yml --web.listen-address=":9095"
open
http://localhost:9095
================
STEP 9 — GRAFANA (VISUALIZATION)
cd C:\Grafana\grafana-13.0.2\bin
.\grafana.exe
open
http://localhost:3000
=================
STEP 10 —  GRAFANA DASHBOARD QUERY
{__name__=~"total_orders_total|success_orders_total|failed_orders_total|retry_orders_total|dlq_orders_total"}
================
ONE CLICK START ULTIMATE SCRIPT CREATE  ( start_full_oms.ps1)
 # CLEAN
taskkill /F /IM python.exe
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker system prune -f

# START DOCKER
cd C:\oms-kafka-event-driven-system
docker compose up -d

Start-Sleep -Seconds 10

# START API
Start-Process powershell -ArgumentList "cd C:\oms-kafka-event-driven-system; python -m uvicorn app.main:app --reload"

# START CONSUMER
Start-Process powershell -ArgumentList "cd C:\oms-kafka-event-driven-system; python consumer_worker.py"

# START PROMETHEUS
Start-Process powershell -ArgumentList "cd C:\Cprometheus; prometheus.exe --config.file=prometheus.yml --web.listen-address=:9095"

# START GRAFANA
Start-Process powershell -ArgumentList "cd C:\Grafana\grafana-13.0.2\bin; grafana.exe"
================
Prometheus (Metrics) — What it REALLY does
👉 Prometheus is your metrics collector
In your OMS project, it tracks:
total orders
success orders
failed orders
retry count
DLQ count
 Simple understanding
Your System → Prometheus → Grafana

Prometheus = collects data
Grafana = shows dashboard
==================
WHERE Prometheus connects in YOUR project
Your FastAPI / Consumer exposes metrics like:
http://localhost:8000/metrics

👉 Prometheus pulls from here
STEP-BY-STEP (CORRECT WAY)
1. Start Prometheus
cd C:\Cprometheus
.\prometheus.exe --config.file=prometheus.yml --web.listen-address=":9095"
2. Open Prometheus UI
http://localhost:9095
3. Verify target (VERY IMPORTANT)
Go to:
http://localhost:9095/targets
You must see:
UP → http://localhost:8000/metrics
.\prometheus.exe --config.file=prometheus.yml --web.listen-address=":9095"
HOW IT CONNECTS TO YOUR PROJECT

When you run:
👉 Newman (1000 records)
Then:
API processes requests
Consumer retries
DLQ triggered
Prometheus collects all counts
👉 Grafana shows graph


=================
Collections - OMS - Event Driven API Testing (Kafka)
body for postman
have to create  POST Create Order (ORDER_PLACED)
=================
{
  "metadata": {
   "event_id": "evt_77a2b9c0-be31-4c6d-9214-5d8f63bb9120",
    "event_type": "ORDER_PLACED",
    "timestamp": "2026-05-31T20:15:30Z",
    "origin_channel": "sasng phone",
    "schema_version": "1.0.0"
  },
  "payload": {
  "order_id":  "ORD1011",
    "customer": {
   "customer_id": "CUST-9921",
      "full_name": "Ramakrishna Jandhyala",
    "email": "ramakrishna@example.com",
      "phone": "+971501234567"
    },
    "financials": {
      "currency": "AED",
      "subtotal": 1234.13,
      "vat_amount": 61.71,
      "shipping_fee": 15.0,
      "grand_total": 1310.84
    },
    "fulfillment": {
      "status": "PLACED",
      "delivery_city": "Dubai",
      "delivery_address": "Apartment 402, Marina Heights, Dubai Marina",
      "estimated_delivery": "2026-06-02"
    },
    "items": [
      {
        "sku": "SKU-TECH-7712",
        "name": "Wireless Noise-Cancelling Headphones",
        "quantity": 1,
        "unit_price": 800.0
      },
      {
        "sku": "SKU-ACC-3341",
        "name": "Fast Charging Dock",
        "quantity": 2,
        "unit_price": 200.0
      }
    ]
  }
}
-----------------------------------------------------------------------------
{
  "metadata": {},
  "payload": {
    "order_id": "{{order_id}}",
    "customer": {
      "customer_id": "{{customer_id}}",
      "full_name": "{{full_name}}",
      "email": "{{email}}",
      "phone": "{{phone}}"
    },
    "items": [
      {
        "sku": "SKU1",
        "name": "{{product_name}}",
        "quantity": {{quantity}},
        "unit_price": {{unit_price}}
      }
    ]
  }
}

==========================

let status = pm.response.code;

// PASS for success
if (status === 200) {
    pm.test("Success Order - 200 OK", function () {
        pm.response.to.have.status(200);
    });
}

// PASS for duplicate
else if (status === 409) {
    pm.test("Duplicate Order handled - 409", function () {
        pm.response.to.have.status(409);
    });
}

// PASS for DLQ / invalid
else if (status === 422) {
    pm.test("Invalid Order sent to DLQ - 422", function () {
        pm.response.to.have.status(422);
    });
}

// FAIL anything unexpected
else {
    pm.test("Unexpected Status Code", function () {
        throw new Error("Unexpected status: " + status);
    });
}

=========================================

env variables 

variable  			   value 
base_url 			   http://localhost:8000
order_id			   ORD-2026-1001
vault:authorization-secret        admin-token-secret