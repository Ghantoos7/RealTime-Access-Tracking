import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from datetime import datetime, timezone,timedelta
from influxdb_client import Point
from utils.config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_URL, INFLUXDB_TOKEN
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


influx_client = InfluxDBClient(url=INFLUXDB_URL,token=INFLUXDB_TOKEN,org=INFLUXDB_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def test_high_frequency_epc():
    """
    Simulates 15 rapid alternating entry/exit events for one EPC.
    """
    epc = "EPC-555"
    now = datetime.now(timezone.utc)
    points = []
    state = "entry"

    for i in range(15):
        state = "exit" if state == "entry" else "entry"
        event_time = now - timedelta(seconds=i * 20)
        point = (
            Point("rfid_event")
            .tag("epc", epc)
            .tag("event", state)
            .tag("direction", "In" if state == "entry" else "Out")
            .tag("door", "2")
            .tag("box", "1")
            .field("rssi", -45)
            .time(event_time)
        )
        points.append(point)

    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=points)
    print("📈 ✅ Inserted 15 high-frequency EPC scan events")


if __name__ == "__main__":
    test_high_frequency_epc()