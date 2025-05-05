import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timezone, timedelta
from influxdb_client import Point
from utils.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_URL, INFLUXDB_TOKEN
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS



influx_client = InfluxDBClient(url=INFLUXDB_URL,token=INFLUXDB_TOKEN,org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def test_never_exited_scenario():
    """
    Simulates an EPC that entered 9 hours ago and never exited.
    """
    event_time = datetime.utcnow().replace(tzinfo=timezone.utc) - timedelta(hours=9)

    point = (
        Point("rfid_event")
        .tag("epc", "EPC-777")
        .tag("event", "entry")
        .tag("direction", "In")
        .tag("door", "3")
        .tag("box", "A")
        .field("rssi", -40)
        .time(event_time)
    )

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=[point])
    print("⏱️ ✅ Inserted simulated 'never exited' entry event")


if __name__ == "__main__":
    test_never_exited_scenario()