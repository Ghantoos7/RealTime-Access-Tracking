
# you might need to change a few of these values depending on your setup

# kafka config
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# topics
TOPIC_RAW_EVENTS = 'rfid-raw-events'
TOPIC_CLEAN_EVENTS = 'rfid-clean-events'
TOPIC_DETECTED_EVENTS = 'rfid-detected-events'

# data 
RAW_EXCEL_PATH = 'data/raw/raw_data.xlsx'
CHOSEN_COLUMNS = ['epc', 'tagtime', 'baselogicaldevice', 'direction', 'rssi']

# Kafka config
GROUP_PREPROCESSING   = "rfid-preprocessing-consumer"
GROUP_DETECTOR = "rfid-detection-consumer"
GROUP_INFLUX_WRITER   = "rfid-influx-writer"


# influxdb config
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "put your token here"
INFLUXDB_ORG = "anexya"
INFLUXDB_BUCKET = "rfid_events"


# mongodb config
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "rfid_pipelines"

# others
MAX_HISTORY = 5
COOLDOWN_MS = 6000
RSSI_THRESHOLD = -60


