
# 🛰️ Real-Time People Access Analytics and Anomaly Detection

## ⚙️ Tech Stack

| Tool            | Purpose                          |
|-----------------|----------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python) | Core scripting language             |
| ![Kafka](https://img.shields.io/badge/Apache%20Kafka-streaming-black?logo=apachekafka) | Data streaming between layers       |
| ![InfluxDB](https://img.shields.io/badge/InfluxDB-timeseries-blue?logo=influxdb) | Time-series database for events     |
| ![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-green?logo=mongodb) | NoSQL storage for raw/clean/history |
| ![Grafana](https://img.shields.io/badge/Grafana-dashboard-orange?logo=grafana) | Dashboards and alerts               |
| ![Docker](https://img.shields.io/badge/Docker-container-blue?logo=docker) | Containerization                    |
| ![VS Code](https://img.shields.io/badge/VSCode-IDE-blue?logo=visualstudiocode) | Development environment             |
| ![Git](https://img.shields.io/badge/Git-version--control-black?logo=git) | Version control                     |



## 📦 Project Structure

```

├── alerts_tests/ # Scripts to simulate alert triggering
│ ├── test_never_exited.py
│ ├── test_night_time.py
│ └── test_rapid_reuse.py
│
├── dashboard/ # Grafana configuration
│ ├── Anomaly Detection.yaml
│ └── People Access Tracking-<ID>.json
│
├── data/ # Place your Excel data files here
├── logs/ # Logs saved from each pipeline
│
├── mongo-data/ 
│
├── pipelines/ # Core pipeline scripts
│ ├── detect_entry_exit_events.py
│ ├── influx_write_events.py
│ ├── ingest_raw_events.py
│ └── preprocess_clean_events.py
│
├── utils/ # Utility modules
│ ├── config.py # Main settings
│ ├── kafka_utils.py
│ ├── logging_utils.py
│ ├── mongo_utils.py
│ └── scoring_utils.py
│
├── main.py # Launches the whole pipeline
├── docker-compose.yml # Docker setup (InfluxDB, Kafka, Grafana)
├── requirements.txt
├── README.md


```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Ghantoos7/RealTime-Access-Tracking
cd RealTime-Access-Tracking
````

### 2. Prepare Data

* Create a `data/` folder in the root directory.
* Place your Excel files containing access data inside it.

### 3. Create InfluxDB Bucket

* Go to your InfluxDB UI → Buckets → Create new
* Name it: `rfid_events`

### 4. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Ensure `requirements.txt` includes:

```
pandas
kafka-python
pymongo
influxdb-client
```

### 5. Update Configuration

Edit `utils/config.py`:

* Replace `INFLUXDB_TOKEN` with your token from InfluxDB.
* Optionally configure MongoDB and Kafka settings.

### 6. Start Services with Docker

```bash
docker-compose up -d
```

This launches:


* Grafana (localhost:3000)
* KafkaUI (localhost:8081)
* InfluxDB (localhost:8086)
* MongoDB (localhost:27017)

---

## 📊 Setup Grafana

1. Go to `http://localhost:3000`
2. Log in (`admin` / `admin`)
3. Add InfluxDB as a data source:

   * URL: `http://influxdb:8086` 
   * Token: Use your configured `INFLUXDB_TOKEN`
   * Bucket: `rfid_events`
4. Import the dashboard JSON:

   * Go to Dashboards → Import → Upload `dashboard/People Access Tracking-1746467770355.json.json`

---

## ⚠️ Configure Alerts

1. Open Grafana → Alerting → Alert rules
2. Import rules from `dashboard/Anomaly Detection.yaml`
3. Ensure notification channels (email, Slack) are configured properly
4. Test alerts by running the data simulation script

---

## 🧪 Running the Pipeline

```bash
python main.py
```

This will launch the entire pipeline:

* Ingest Excel → Kafka
* Clean → Kafka
* Detect → Kafka
* Write → InfluxDB
* Store in MongoDB

---

## 🧠 Useful Tips

* All logs are written to `rfid_stream.log` for easier debugging.
* Each processing layer logs events, exceptions, and stats.
* MongoDB contains raw, clean, and detected event collections for history/auditing.
* Use Grafana for real-time anomaly monitoring.

---

## 🧼 Stopping Everything

```bash
docker-compose down
```

---

## 📝 License

This project is licensed under MIT License.

---
