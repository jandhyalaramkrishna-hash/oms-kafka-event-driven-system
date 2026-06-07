import json
from kafka import KafkaConsumer

KAFKA_BROKER = "localhost:9092"
DLQ_TOPIC = "orders_dlq"

consumer = KafkaConsumer(
    DLQ_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="dlq-monitor-group"
)

print("🚨 Listening to DLQ...")

for message in consumer:
    print("\n🔥 DLQ MESSAGE RECEIVED:")
    print(json.dumps(message.value, indent=4))