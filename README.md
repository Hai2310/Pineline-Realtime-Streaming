# PIPELINE-REALTIME-STREAMING — IoT Device Data Streaming & Analytics  

## 📖 Overview  
This project implements a real-time data streaming pipeline that collects and processes IoT device data through a full chain of technologies:  
**Kafka → Spark Streaming → PostgreSQL → Power BI**

The system simulates real IoT devices sending JSON data, streams it via **Apache Kafka**, processes and aggregates it in **Apache Spark**, and stores the results in a **PostgreSQL** database.  
Finally, the data is visualized in a **live Power BI dashboard** for monitoring device performance and detecting late or missing data.

---

## 🧩 System Architecture  


+-------------+       +-----------+        +------------------+        +----------------+
|  IoT Device | --->  |   Kafka   | --->   | Spark Structured  | --->  |  PostgreSQL DB |
| (JSON Data) |       |  Producer |        |     Streaming     |       | (Data Storage) |
+-------------+       +-----------+        +------------------+        +----------------+
                                                                       |
                                                                       v
                                                                +---------------+
                                                                | Power BI Live |
                                                                |  Dashboard    |
                                                                +---------------+
## 📁 PIPELINE-REALTIME-STREAMING/
├── checkpoint_dir_kafka/         # Spark Streaming checkpoint directory
├── devices/                      # Simulated IoT devices and data samples
│   ├── device_01.json
│   ├── device_02.json
│   ├── device_03.json
│   ├── device_data_samples.txt
│   └── late_data_samples.txt
├── kafka/                        # Kafka producer & event handling
│   ├── device_events.py          # Simulate device data and send to Kafka topic
│   └── post_kafka.py             # Producer posting real or synthetic events
├── report/
│   └── device_dashboard.pbix     # Power BI dashboard for real-time visualization
├── venv/                         # Virtual environment for Python dependencies
├── postgresql-42.7.3.jar         # PostgreSQL JDBC driver for Spark connection
├── spark_streaming.ipynb         # Spark Streaming job: consume, transform & store
├── .gitignore
└── README.md
## 💾 Example Input (Kafka JSON Event)
{
  "eventId": "e3cb26d3-41b2-49a2-84f3-0156ed8d7502",
  "eventOffset": 10001,
  "eventPublisher": "device",
  "customerId": "CI00103",
  "data": {
    "devices": [
      { "deviceId": "D001", "temperature": 15, "measure": "C", "status": "ERROR" },
      { "deviceId": "D002", "temperature": 16, "measure": "C", "status": "SUCCESS" }
    ]
  },
  "eventTime": "2023-01-05 11:13:53.643364"
}

📊 Example Output (After Spark Processing)

| customerId | eventId         | eventOffset | eventPublisher | eventTime               | deviceId | measure status  | temperature |
| ---------- | ------------------------------------ | ----------- | -------------- | ----------------------- | -------- | ------- | ------- | ----------- |
| CI00190    | 2f472dee-b4b2-4d3b-bc2b-03f39ed24c1e | 10238 | device | 2025-10-29 18:30:00.000 | D002     | C       SUCCESS |44     |
| CI00190    | 2f472dee-b4b2-4d3b-bc2b-03f39ed24c1e | 10238      | device         | 2025-10-29 18:30:00.000 | D004     | C       | STANDBY | 6           |
| CI00190    | 2f472dee-b4b2-4d3b-bc2b-03f39ed24c1e | 10238       | device         | 2025-10-29 18:30:00.000 | D008     | C       | SUCCESS | 25          |

🗄️ PostgreSQL Table Schema

CREATE TABLE iot_device_events (
    eventId UUID PRIMARY KEY,
    customerId VARCHAR(20),
    eventOffset BIGINT,
    eventPublisher VARCHAR(50),
    eventTime TIMESTAMP,
    deviceId VARCHAR(20),
    measure VARCHAR(10),
    status VARCHAR(20),
    temperature FLOAT
);

✅ Notes:

eventId uniquely identifies each event (UUID).

temperature and measure capture IoT sensor readings.

The pipeline flattens nested JSON (data.devices) into row-level records per device.

## ⚙️ Components Description
1️⃣ Kafka Layer (Data Ingestion)

Located in: /kafka/

device_events.py

Simulates continuous IoT device data (e.g., temperature, pressure, humidity).

Publishes events to a Kafka topic (e.g., device_stream).

post_kafka.py

Acts as Kafka Producer.

Handles event publishing and retry logic for real/simulated devices.

2️⃣ Spark Streaming Layer (Data Processing)

Located in: spark_streaming.ipynb

Reads JSON events from Kafka in real-time.

Parses nested JSON → flattens devices[] array.

Performs transformations (filtering, aggregations, late event handling).

Writes clean structured data into PostgreSQL.

3️⃣ PostgreSQL Layer (Data Storage)

Stores transformed device records.

Used as a source for Power BI dashboard.

JDBC connection configured via postgresql-42.7.3.jar.

4️⃣ Power BI Layer (Visualization)

File: /report/device_dashboard.pbix

Connects to PostgreSQL DB in DirectQuery mode.

Displays metrics such as:

Device status distribution (SUCCESS, ERROR, STANDBY)

Average temperature by device

Real-time stream refresh

## 🧠 Example Workflow

Producer: device_events.py simulates IoT data and pushes JSON to Kafka.

Stream Processor: Spark reads Kafka stream (spark_streaming.ipynb).

Database Storage: Clean data saved to PostgreSQL (iot_device_events table).

Dashboard: Power BI connects to PostgreSQL for live insights.

🧰 Tech Stack
Layer	Technology
Data Ingestion	Apache Kafka
Stream Processing	Apache Spark Structured Streaming
Storage	PostgreSQL
Visualization	Power BI
Language	Python 3.10
Driver	postgresql-42.7.3.jar
🚀 How to Run

Start Kafka & Zookeeper

zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties
kafka-topics.sh --create --topic device_stream --bootstrap-server localhost:9092


Run Kafka Producer

python kafka/device_events.py


Run Spark Streaming

pyspark --jars postgresql-42.7.3.jar
# or run spark_streaming.ipynb in Jupyter


Visualize in Power BI

Open report/device_dashboard.pbix

Connect to PostgreSQL → table iot_device_events

Refresh dashboard in real-time.

## 🚀 Key Features

✅ Real-time data ingestion with Apache Kafka ✅ Fault-tolerant, scalable stream processing using Spark Structured Streaming ✅ Reliable persistence using PostgreSQL JDBC ✅ Real-time dashboard visualization in Power BI ✅ Support for late data handling and checkpointing ✅ Modular codebase for easy extension to new device types

## 🧠 Future Improvements

Integrate machine learning anomaly detection models in Spark.

Deploy the pipeline on Kubernetes or Databricks.

Add Grafana dashboard for alternative visualization.

Implement REST API for querying latest device status.

## 👨‍💻 Author

Hoàng Minh Hải - minhhaiit1k68@gmail.com