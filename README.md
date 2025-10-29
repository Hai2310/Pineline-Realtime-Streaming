⚡ PIPELINE-REALTIME-STREAMING — IoT Device Data Streaming & Analytics
📖 Overview

This project implements a real-time data streaming pipeline that collects and processes IoT device data through a full chain of technologies:
Kafka → Spark Streaming → PostgreSQL → Power BI.

The system simulates real IoT devices sending JSON data, streams it via Apache Kafka, processes and aggregates it in Apache Spark, and stores the results in a PostgreSQL database.
Finally, the data is visualized in a live Power BI dashboard for monitoring device performance and detecting late or missing data.

🏗️ System Architecture
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

📂 Project Structure
PIPELINE-REALTIME-STREAMING/
│
├── checkpoint_dir_kafka/              # Spark Streaming checkpoint directory
│
├── devices/                           # Simulated IoT devices and data samples
│   ├── device_01.json
│   ├── device_02.json
│   ├── device_03.json
│   ├── device_data_samples.txt
│   └── late_data_samples.txt
│
├── kafka/                             # Kafka producer & event handling
│   ├── device_events.py               # Simulate device data and send to Kafka topic
│   └── post_kafka.py                  # Producer posting real or synthetic events
│
├── report/
│   └── device_dashboard.pbix          # Power BI dashboard for real-time visualization
│
├── venv/                              # Virtual environment for Python dependencies
│
├── postgresql-42.7.3.jar              # PostgreSQL JDBC driver for Spark connection
├── spark_streaming.ipynb              # Spark Streaming job: consume, transform & store
├── .gitignore
└── README.md

🔧 Components Description
1️⃣ Kafka Layer (Data Ingestion)

Located in /kafka/

device_events.py

Simulates continuous IoT device data (e.g., temperature, pressure, humidity).

Publishes events to a Kafka topic (e.g., device_stream).

post_kafka.py

Posts JSON-formatted data to Kafka in real time.

Handles both regular and “late” data to test stream tolerance.

📘 Example JSON message:

{
  "eventId": "e3cb26d3-41b2-49a2-84f3-0156ed8d7502",
  "eventOffset": 10001,
  "eventPublisher": "device",
  "customerId": "CI00103",
  "data": {
    "devices": [
      {
        "deviceId": "D001",
        "temperature": 15,
        "measure": "C",
        "status": "ERROR"
      },
      {
        "deviceId": "D002",
        "temperature": 16,
        "measure": "C",
        "status": "SUCCESS"
      }
    ]
  },
  "eventTime": "2023-01-05 11:13:53.643364"
}
2️⃣ Spark Structured Streaming (Processing Layer)

File: spark_streaming.ipynb

Reads live data from the Kafka topic.

Parses JSON payloads and extracts key fields.

Applies windowed aggregation and watermarking to manage late-arriving events.

Writes transformed data to PostgreSQL in real time.

📘 Example tasks handled:

Detect missing/lost device signals.

Compute rolling averages (e.g., temperature per minute).

Save results using JDBC connection via postgresql-42.7.3.jar.

3️⃣ PostgreSQL (Storage Layer)

Acts as the persistent storage for processed data.

Schema may include:

CREATE TABLE device_readings (
    device_id VARCHAR(50),
    event_time TIMESTAMP,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    status VARCHAR(20),
    processed_at TIMESTAMP
);


Data inserted directly from Spark in streaming mode.

4️⃣ Power BI Dashboard (Visualization Layer)

File: report/device_dashboard.pbix

Connects to PostgreSQL database for real-time data refresh.

Displays metrics such as:

Device activity timeline

Average temperature & humidity per device

Alerts for offline or delayed data

💡 The dashboard provides real-time monitoring for IoT device health and data latency.

⚙️ Setup Instructions
1️⃣ Environment Setup
python -m venv venv
source venv/bin/activate   # (on Linux/Mac)
venv\Scripts\activate      # (on Windows)

pip install -r requirements.txt

2️⃣ Start Kafka & Zookeeper
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties

3️⃣ Create Kafka Topic
kafka-topics.sh --create --topic device_stream --bootstrap-server localhost:9092

4️⃣ Run the Kafka Producer
python kafka/device_events.py

5️⃣ Run the Spark Streaming Job
jupyter notebook spark_streaming.ipynb

6️⃣ Check Data in PostgreSQL
SELECT * FROM device_readings ORDER BY event_time DESC;

7️⃣ Open Power BI Report

Load device_dashboard.pbix

Connect to PostgreSQL

Enable real-time refresh

📊 Example Output
customerId	   eventId	                       eventOffset	eventPublisher	eventTime	        deviceId	measure	status	temperature
CI00103	e3cb26d3-41b2-49a2-84f3-0156ed8d7502	    10001	device	2023-01-05 11:13:53.643364	  D001	        C	ERROR	15
CI00103	e3cb26d3-41b2-49a2-84f3-0156ed8d7502	    10001	device	2023-01-05 11:13:53.643364	  D002	        C	SUCCESS	16
CI00190	2f472dee-b4b2-4d3a-b1c4-16dd54a2cf62	    10238	device	2025-10-29 18:30:01.654321	  D002	        C	SUCCESS	44
CI00190	2f472dee-b4b2-4d3a-b1c4-16dd54a2cf62	    10238	device	2025-10-29 18:30:01.654321	  D004	        C	STRANDBY	6
CI00190	2f472dee-b4b2-4d3a-b1c4-16dd54a2cf62	    10238	device	2025-10-29 18:30:01.654321	  D008	        C	SUCCESS	25
🚀 Key Features

✅ Real-time data ingestion with Apache Kafka
✅ Fault-tolerant, scalable stream processing using Spark Structured Streaming
✅ Reliable persistence using PostgreSQL JDBC
✅ Real-time dashboard visualization in Power BI
✅ Support for late data handling and checkpointing
✅ Modular codebase for easy extension to new device types

🧠 Future Improvements

Integrate machine learning anomaly detection models in Spark.

Deploy the pipeline on Kubernetes or Databricks.

Add Grafana dashboard for alternative visualization.

Implement REST API for querying latest device status.

👨‍💻 Author

Hoàng Minh Hải - minhhaiit1k68@gmail.com