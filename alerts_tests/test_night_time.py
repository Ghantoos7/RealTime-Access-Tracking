
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timezone
from influxdb_client import Point
from utils.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_URL, INFLUXDB_TOKEN
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


influx_client = InfluxDBClient(url=INFLUXDB_URL,token=INFLUXDB_TOKEN,org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def test_entry_before_6am():
    """
    Simulates an entry event at 3 AM and writes to InfluxDB.
    """
    now = datetime.now(timezone.utc)
    event_time = now.replace(hour=1, minute=21, second=0, microsecond=0)

    point = (
        Point("rfid_event")
        .tag("epc", "EPC-999")
        .tag("event", "entry")
        .tag("direction", "In")
        .tag("door", "1")
        .tag("box", "4")
        .field("rssi", -55)
        .time(event_time)
    )

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=[point])
    print("🌙 ✅ Inserted simulated night entry event")


if __name__ == "__main__":
    test_entry_before_6am()