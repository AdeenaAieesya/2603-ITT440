# 2603-ITT440

# DISTRIBUTED CLIENT-SERVER ARCHITECTURE WITH REAL-TIME WEB CENTRALIZED MONITORING

# INTRODUCTION
In modern networked systems, decentralized applications rely heavily on robust, distributed communication protocols to synchronize data across heterogeneous nodes. This project demonstrates the implementation of a cross-platform, distributed client-server ecosystem designed to aggregate real-time performance indicators or metrics across multiple local workstation nodes (Laptop 1 through Laptop 6).

The system utilizes a hybrid program composition combining:
**Low-level Primitive C Sockets for high-efficiency, lightweight socket manipulation**
**High-level Python Multi-Threaded Sockets for robust concurrency handling and database transactions**

The central component of the topology sits on Laptop 1 (Adeena) , acting as the structural core. Laptop 1:
**Aggregates cross-network updates via an operational socket framework**
**Persists real-time metric streams directly into a centralized MySQL database subsystem**
**Presents a dynamic user interface via an integrated Flask Web Monitor Dashboard**

The entire layout is orchestrated natively using containerized infrastructure via Docker Compose to maintain platform decoupling and environment portability.

# OBJECTIVES
The project successfully implements:
 - 3 types of containers: Database, Server, and Client
 - Multi-language socket communication: C and Python
 - Live web dashboard: Real-time leaderboard with auto-refresh
 - Centralized database: MySQL 8.0 for storing user points
 - Scalable architecture: All containers on the same Docker network


# FEATURES
* **Multi-Language Sockets:** Real-time data exchange between C and Python using TCP Sockets 
* **Distributed Nodes:** 6 laptops (nodes) communicating through a central database
* **Dockerized:** 	Fully isolated services within a secure internal network
* **Live Dashboard:** Flask web application with auto-refresh every 2 seconds
* **Central Database:** MySQL 8.0 for robust data logging
* **Horizontal Scaling:** Easily scale up containerized servers and clients
* **Real-time Updates:** Points update every 30 seconds


# SYSTEM REQUIREMENTS
* **Operating System:** Kali Linux (WSL2) / Ubuntu / Any Linux distribution
* **Containerization:** Docker Engine v20.10+ & Docker Compose v2.20+
* **Compiler:** GCC (for C compilation)
* **Programming Language:** Python 3.9+
* **Network:** All laptops connected to the same hotspot
* **Hardware:** x86_64 or ARM64 architecture
* **Ports Required:** 3306 (MySQL), 5000 (Dashboard), 8080-8084 (Servers)
* **Database:** MySQL 8.0


# HOW TO SETUP AND RUN FOR LAPTOP 1 (CENTRAL HUB)
##1. Clone the Repository
```bash
git clone https://github.com/AdeenaAieesya/ITT440-Group-Project.git
cd ITT440-Group-Project
```

##2. Navigate to the project folder
```bash
cd ~/itt440-laptop1
```

##3. Start Docker containers
```bash
docker compose -f docker-compose-laptop1.yml up -d
```
<img width="936" height="185" alt="image" src="https://github.com/user-attachments/assets/77bf97aa-b1d4-4306-90a3-a9e618d9a073" />

##4. Initialize the database
```bash
docker exec -i itt440-db mysql -u root -psecretpass library_stats < database/init.sql
```

##5. Verify database
```bash
docker exec itt440-db mysql -u root -psecretpass -e "SELECT * FROM library_stats.segmen_mata;"
```
<img width="936" height="296" alt="image" src="https://github.com/user-attachments/assets/1548ccc1-cecb-4641-b3c4-7c1926905e55" />



# HOW TO SETUP AND RUN FOR LAPTOP 2-6 
```bash
# Navigate to the respective folder
cd C:\itt440-mastura-docker   # Laptop 2
# OR
cd C:\itt440-azra-docker      # Laptop 3
# OR
cd C:\itt440-aina-docker      # Laptop 4
# OR
cd C:\itt440-fasihah-docker   # Laptop 5
# OR
cd C:\itt440-irdina-docker    # Laptop 6

# Build and start containers
docker compose build
docker compose up -d
```


# HOW TO RUN WEB DASHBOARD
FOR LAPTOP 1:
```bash
http://localhost:5000
```
<img width="1918" height="687" alt="Screenshot 2026-07-12 211143" src="https://github.com/user-attachments/assets/8b6f5038-7bef-4f96-ac2e-a455bbaf5081" />


FOR OTHER LAPTOPS:
```bash
http://192.168.43.248:5000
```


#DEPLOYMENT AND MONITORING
<img width="938" height="395" alt="image" src="https://github.com/user-attachments/assets/db368634-512f-47ce-88ea-98abfb714b72" />

## Monitoring C Server Logs
<img width="826" height="533" alt="Screenshot 2026-07-12 220508" src="https://github.com/user-attachments/assets/41f014f7-7230-4628-9644-09803963acaf" />

## Monitoring C Client Logs
<img width="723" height="188" alt="Screenshot 2026-07-03 025457" src="https://github.com/user-attachments/assets/b360e0e1-7dcd-4db2-8944-091c423f18ac" />

## How to run specific containers
```bash
# Monitor a specific container
docker logs -f mastura-server

# Monitor all Python clients
docker compose logs -f | grep "Python Client"

# Monitor all C clients
docker compose logs -f | grep "C Client"
```


# SYSTEM ARCHITECTURE & TOPOLOGY
| Laptop | Containers | Type | Port |
|-------------|---------------|------------|------------|
| Laptop 1 (Adeena)     | 4 containers    | C (Real)     |  8080     |
| Laptop 2 (Mastura)         | 2 containers    | Python (C-Label)     |  8082     |
| Laptop 3 (Azra)         | 2 containers    | Python (C-Label)     |  8082     |
| Laptop 4 (Aina)         | 2 containers    | Python     |  8084    |
| Laptop 5 (Fasihah)         | 2 containers    | C (Real)     |  8083     |
| Laptop 6 (Irdina)         | 2 containers    | Python      |  8084    |


# COMMUNICATION FLOW
┌──────────┐    ┌──────────┐    ┌──────────┐
│  CLIENT  │───>│  SERVER  │───>│  DATABASE│
│  "PING"  │    │  UPDATE  │    │  +3 pts  │
│          │<───│   "OK"   │    │          │
└──────────┘    └──────────┘    └──────────┘


# METHODOLOGY & TECHNICAL SOURCE CODE
## Central Infrastructure Design (Laptop 1 - Adeena)
Multi-Service Compose Orchestration (docker-compose-laptop1.yml)
The orchestration configuration specifies strict service dependencies, requiring successful execution of health checks within the relational engine before spinning up dependent application workers.

## Database Schema Blueprint (init.sql)
The persistent storage uses a structure containing indexing constraints for efficient database query reads during live data polls from the web client interface.

## Central Web Visualizer Monitor Component (monitor.py)
Developed using a lightweight Python Flask framework to avoid heavy rendering overhead. It performs asynchronous data fetching and returns clean dashboard views that auto-refresh every 2000ms.

# DISTRIBUTED DATA ANALYSIS & RESULTS
Once all containers were launched, real-time metrics generation was confirmed across the network. The dashboard compiled data using sequential SQL sort operations, verifying successful distributed telemetry insertion.


## Performance Insights and Concurrency Handling
### 1. Low-Level Thread Execution Stability: 
The native C implementation on Laptop 1 and Laptop 5 demonstrated minimal CPU clock latency. Memory locks remained constant under persistent multi-threaded payload hits because the C applications isolate database writes into independent worker threads (pthread_create).

### 2. Cross-Platform Networking Consistency: 
The hybrid platform communication was stable. Python sockets gracefully marshaled input requests into string objects, while the lower-level C applications received them as standard character buffers (char buffer[1024]). This demonstrates that cross-language systems can interact seamlessly as long as they follow standard TCP streaming byte boundaries.

### 3. Relational Integrity Maintenance: 
Using standard database connection pools (pymysql.connect and mysql_real_connect) verified that atomic mutations correctly maintained ACID compliance across multiple client requests. This prevented row contention issues, even when multiple external workstations updated the table simultaneously.


# CONCLUSION 
This project successfully demonstrates a containerized, cross-platform distributed network monitor architecture. Separating computational workloads into functional microservices managed by Docker Compose resolved previous environment configuration problems, such as localized missing package dependencies.
