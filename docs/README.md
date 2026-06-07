# OMS Kafka Event-Driven System (QA Automation Project)

##Overview

This project demonstrates a **real-time event-driven microservices architecture** using:

* FastAPI (Producer API)
* Apache Kafka (Event Streaming)
* Consumer with Retry & DLQ (Dead Letter Queue)
* Newman (API Automation Testing)
* Allure (Test Reporting)
* Prometheus & Grafana (Monitoring & Visualization)

---

## Key Features

* ✅ Event-driven order processing
* ✅ Idempotency (duplicate order handling)
* ✅ Retry mechanism with max attempts
* ✅ Dead Letter Queue (DLQ) for failed messages
* ✅ Automated API testing with 1000+ records
* ✅ Beautiful test reports (Newman + Allure)
* ✅ Real-time monitoring (Prometheus + Grafana)

---

## Project Structure

```
oms-kafka-event-driven-system/
│
├── app/                # FastAPI Producer
├── consumer/           # Kafka Consumer (Retry + DLQ)
├── producer/           # Optional Producer logic
├── testdata/           # CSV test data (1000 records)
├── newman/             # Test reports
├── monitoring/         # Prometheus config
├── scripts-run-project/# Automation scripts
├── docker-compose.yml  # Kafka setup
├── README.md
```

---

## Prerequisites

Install once:

```
npm install -g newman
npm install -g newman-reporter-html newman-reporter-json
npm install -g allure-commandline
```

Also install:

* Docker Desktop
* Python 3.x

---

## One-Click Execution

Run the full system:

```
cd scripts-run-project
.\start_oms.ps1
```

This will:

* Stop old processes
* Start Kafka, Zookeeper, Prometheus
* Start FastAPI (Producer)
* Start Consumer
* Run Newman (1000 records)
* Generate HTML report
* Generate Allure report
* Open Swagger UI
* Open Prometheus & Grafana dashboards

---

## API Endpoint

### Create Order

```
POST /orders
http://localhost:8000/orders
```

---

## Test Automation (Newman)

Runs 1000 test records:

* ✔ Success → 200
* ✔ Duplicate → 409
* ✔ Invalid → 422 (DLQ)

---

## Monitoring

### Prometheus

```
http://localhost:9091
```

### Grafana

```
http://localhost:3000
```

### Metrics Collected

* total_orders_total
* success_orders_total
* failed_orders_total
* retry_orders_total
* dlq_orders_total

---

## DLQ Verification

```
docker exec -it kafka kafka-console-consumer \
--topic orders_dlq \
--from-beginning \
--bootstrap-server localhost:9092
```

---

## Allure Report

```
allure open newman/allure-report
```

---

## Interview Highlights

This project demonstrates:

* Event-driven architecture using Kafka
* Fault tolerance with Retry & DLQ
* API automation using Newman
* Test reporting using Allure
* Monitoring using Prometheus & Grafana

---

## Author

Ramakrishna Jandhyala
QA Automation Engineer
