=====================================================================
🚀 SWADESI ENTERPRISES OMS - ALL-IN-ONE PIPELINE GUIDE
=====================================================================

[STEP 1] ENVIRONMENT RESET & RUNTIME START:
Opening an Administrator PowerShell window, heading into this folder, and firing our automation controller script:
  cd C:\oms-kafka-event-driven-system\GEmini
  .\start_complete_pipeline.ps1

[STEP 2] NEWMAN DATA SUITE EXECUTION:
Once the 70-second countdown stabilizer completes and your 6 application windows are live, move back to your main directory window and launch the 1,000-record test suite:
  cd C:\oms-kafka-event-driven-system
  newman run testdata\OMS-postman_collection.json -e testdata\OMS-postman_environment.json -d testdata\oms_1000_records.csv -r cli,html,json --reporter-html-export report.html --reporter-json-export report.json

[STEP 3] DASHBOARD MONITORING OBSERVABILITY:
  * Prometheus Server metrics panel: http://localhost:9095
  * Grafana Core analytical graphs:  http://localhost:3000 (admin / admin)