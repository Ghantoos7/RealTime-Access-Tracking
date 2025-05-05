from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from utils import create_consumer, get_logger
from utils import TOPIC_DETECTED_EVENTS, GROUP_INFLUX_WRITER, INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

logger = get_logger("[INFLUX_WRITER]", "rfid_stream.log")

def write_detected_events_to_influx():
    """
    Consumes detected RFID entry/exit events from Kafka and writes them to InfluxDB.
    """
    logger.info("STARTED - action=kafka_to_influx topic=rfid-detected-events")

    consumer = create_consumer(topic=TOPIC_DETECTED_EVENTS,group_id=GROUP_INFLUX_WRITER,auto_offset_reset='latest')
    
    influx_client = InfluxDBClient(url=INFLUXDB_URL,token=INFLUXDB_TOKEN,org=INFLUXDB_ORG)
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    for msg in consumer:
        data = msg.value

        epc = data.get('epc')
        direction = data.get('direction')
        event_type = data.get('event')
        rssi = data.get('rssi')
        timestamp = data.get('timestamp')
        door = data.get('door')
        box = data.get('box')

        if None in [epc, direction, event_type, rssi, timestamp]:
            logger.warning(f"SKIPPED - reason=missing_fields data={data}")
            continue

        try:
            event_time = datetime.fromisoformat(timestamp)

            point = (
                Point("rfid_event")
                .tag("epc", str(epc))
                .tag("event", str(event_type))
                .tag("direction", str(direction))
                .tag("door", str(door or "unknown"))
                .tag("box", str(box or "unknown"))
                .field("rssi", float(rssi))
                .time(event_time)
            )

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            logger.info(f"WRITTEN - epc={epc} event={event_type} direction={direction} door={door} rssi={rssi} time={timestamp}")

        except Exception as e:
            logger.error(f"FAILED - reason={e} data={data}")

if __name__ == "__main__":
    write_detected_events_to_influx()
