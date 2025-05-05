from datetime import datetime, timezone
from utils import TOPIC_RAW_EVENTS, TOPIC_CLEAN_EVENTS, GROUP_PREPROCESSING
from utils import create_producer, create_consumer, get_logger, get_mongo_collection


mongo_col = get_mongo_collection("clean_events")
logger = get_logger("[PREPROCESSING]", "rfid_stream.log")

def start_cleaning_pipeline():
    """
    Consumes raw RFID events from Kafka, validates and cleans them, and sends to the clean topic.
    """
    logger.info("STARTED - action=preprocessing_consumer topic=raw_events")

    producer = create_producer()
    consumer = create_consumer(TOPIC_RAW_EVENTS, group_id=GROUP_PREPROCESSING)

    for msg in consumer:
        raw = msg.value

        try:
            epc = str(raw.get("epc", "")).strip()
            location = str(raw.get("baselogicaldevice", "")).strip()
            tagtime = int(float(raw["tagtime"]))
            if not epc or not location or not tagtime:
                logger.warning(f"SKIPPED - reason=missing_fields epc={epc} location={location} tagtime={tagtime}")
                continue

            direction = str(raw.get("direction", "")).strip().capitalize()
            rssi = float(raw.get("rssi", -999))
            timestamp_iso = datetime.fromtimestamp(tagtime / 1000, tz=timezone.utc).isoformat()
            location_parts = location.split("_")
            door = str(location_parts[3][4])
            box = str(location_parts[4][3])

            clean_event = {
                "epc": epc,
                "direction": direction,
                "door": door,
                "box": box,
                "rssi": rssi,
                "tagtime": tagtime,
                "timestamp": timestamp_iso
            }

            producer.send(TOPIC_CLEAN_EVENTS, clean_event)
            logger.debug(f"SENT - epc={epc} tagtime={tagtime} rssi={rssi}")
            mongo_col.insert_one(clean_event)


        except Exception as e:
            logger.error(f"FAILED - reason={e} raw={raw}")

    producer.flush()
    logger.info("COMPLETED - action=preprocessing_flush")

if __name__ == "__main__":
    start_cleaning_pipeline()
