import json
import time
import logging
from kafka import KafkaConsumer, KafkaProducer
from logger_config import setup_logger
from prometheus_client import start_http_server, Counter
from email_service import send_email

# ================= LOGGING =================
setup_logger()
logger = logging.getLogger(__name__)

# ================= PROMETHEUS METRICS =================
TOTAL_ORDERS = Counter('total_orders', 'Total Orders Processed')
SUCCESS_ORDERS = Counter('success_orders', 'Successful Orders')
FAILED_ORDERS = Counter('failed_orders', 'Failed Orders')
RETRY_ORDERS = Counter('retry_orders', 'Retry Attempts')
DLQ_ORDERS = Counter('dlq_orders', 'Orders sent to DLQ')

# Start Prometheus metrics server
start_http_server(8001)
logger.info("Prometheus metrics running at http://localhost:8001")

# ================= CONFIG =================
KAFKA_BROKER = "localhost:9092"
ORDERS_TOPIC = "orders"
DLQ_TOPIC = "orders_dlq"
MAX_RETRIES = 3

# ================= KAFKA =================
consumer = KafkaConsumer(
    ORDERS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="order-consumer-group"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

logger.info("Kafka Consumer started")

# ================= PROCESS FUNCTION =================
def process_order(order):
    payload = order.get("payload", {})
    order_id = payload.get("order_id")

    logger.info(f"Received Order: {order}")

    if not payload:
        raise Exception("Invalid payload structure")

    # --- INVALID PRODUCT DETECTION BLOCK ---
    items = payload.get("items", [])
    for item in items:
        if "InvalidProduct" in item.get("name", ""):
            print("❌ Invalid product detected → sending to DLQ")
            raise Exception("Invalid product detected")

    # Simulated failures
    if order_id == "ORD222":
        raise Exception("Database error: Duplicate entry")

    if order_id == "ORD333":
        raise Exception("Payment service timeout")

    if order_id == "ORD999":
        raise Exception("Random processing failure")

    logger.info(f"Order processed successfully: {order_id}")

# ================= CONSUMER LOOP =================
for message in consumer:
    order = message.value
    if not order:
        continue

    payload = order.get("payload", {})
    order_id = payload.get("order_id")

    TOTAL_ORDERS.inc()

    try:
        # Try processing the incoming order
        process_order(order)
        SUCCESS_ORDERS.inc()

        # ✅ EMAIL FOR SUCCESS (ONLY SPECIFIC RECORD)
        if order_id == "ORD0001":
            send_email(
                "Order Success",
                f"Order {order_id} processed successfully",
                "jandhyala.ramkrishna@gmail.com"
            )

    except Exception as e:
        print("⚠️ Error occurred:", str(e))
        logger.error(f"Processing failed: {str(e)}")
        FAILED_ORDERS.inc()

        retries = order.get("retries", 0)

        # Check if we should retry or route directly to DLQ
        if retries < MAX_RETRIES:
            logger.warning(f"Retrying... Attempt {retries + 1}")
            RETRY_ORDERS.inc()

            retry_payload = order.copy()
            retry_payload["retries"] = retries + 1

            time.sleep(2)
            producer.send(ORDERS_TOPIC, retry_payload)
            producer.flush()  # Ensures the message is fully pushed out before moving on

        else:
            # ================= DLQ BLOCK EXECUTING =================
            logger.critical("Max retries reached -> Sending to DLQ")
            DLQ_ORDERS.inc()

            dlq_payload = {
                "failed_message": order,
                "error": str(e),
                "failed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Send payload metadata to DLQ Topic
            producer.send(DLQ_TOPIC, dlq_payload)
            producer.flush()

            # ✅ DLQ EMAIL TRIGGER
            print(f"📧 Attempting to dispatch failure alert email for Order: {order_id}")
            send_email(
                "Order Execution Failure - Sent to DLQ",
                f"Alert: Order {order_id} dropped out of pipeline.\nReason: {str(e)}",
                "jandhyala.ramkrishna@gmail.com"
            )