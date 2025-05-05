from kafka import KafkaConsumer, KafkaProducer
import json
from .config import KAFKA_BOOTSTRAP_SERVERS

def create_producer():
    """
    Creates a Kafka producer with JSON serialization.
    """
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def create_consumer(topic, group_id, auto_offset_reset='latest'):
    """
    Creates a Kafka consumer for the given topic and group.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
