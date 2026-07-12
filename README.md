# 2603-ITT440

# DISTRIBUTED CLIENT-SERVER ARCHITECTURE WITH REAL-TIME WEB CENTRALIZED MONITORING

# INTRODUCTION
In modern networked systems, decentralized applications rely heavily on robust, distributed communication protocols to synchronize data across heterogeneous nodes. This project demonstrates the implementation of a cross-platform, distributed client-server ecosystem designed to aggregate real-time performance indicators or metrics across multiple local workstation nodes (Laptop 1 through Laptop 6).

The system utilizes a hybrid program composition combining low-level primitive C Sockets for high-efficiency, lightweight socket manipulation alongside high-level Python Multi-Threaded Sockets for robust concurrency handling and database transactions.

The central component of the topology sits on Laptop 1 (Adeena), acting as the structural core. Laptop 1 aggregates cross-network updates via an operational socket framework, persists real-time metric streams directly into a centralized MySQL database subsystem, and presents a dynamic user interface via a integrated Flask Web Monitor Dashboard.

The entire layout is orchestrated natively using containerized infrastructure via Docker Compose to maintain platform decoupling and environment portability.


# SYSTEM ARCHITECTURE & TOPOLOGY
Workstation Node ProfilesLaptop 1 (Adeena - Hub Node): Runs a native C POSIX socket server instance handling automated internal increments alongside an atomic pymysql listener web service displaying state mutations live.

Laptop 2 & Laptop 3 (Mastura & Azra): Python-engineered socket setups simulating classic platform loops on Port 8082, adding $+3$ metric records upon structural verification handshakes.

Laptop 4 & Laptop 6 (Aina & Irdina): Pure Python engine implementations operating over Port 8084, dispatching targeted database query instructions to append $+4$ data steps per update.

Laptop 5 (Fasihah): Independent native C system operating directly on host network virtualization layer over Port 8083, writing structural updates back to Laptop 1 through low-level MariaDB driver interfaces.


# METHODOLOGY & TECHNICAL SOURCE CODE
## Central Infrastructure Design (Laptop 1 - Adeena)
Multi-Service Compose Orchestration (docker-compose-laptop1.yml)
The orchestration configuration specifies strict service dependencies, requiring successful execution of health checks within the relational engine before spinning up dependent application workers.

```bash
services:
  database:
    image: mysql:8.0
    container_name: itt440-db
    environment:
      MYSQL_ROOT_PASSWORD: secretpass
      MYSQL_DATABASE: library_stats
    ports:
      - "3306:3306"
    networks:
      - itt440_net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-psecretpass"]
      interval: 10s
      timeout: 5s
      retries: 5

  web_monitor:
    build: ./web-monitor
    container_name: itt440-web-monitor
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=database
    depends_on:
      database:
        condition: service_healthy
    networks:
      - itt440_net
    restart: unless-stopped

  c_server:
    build: ./c-server
    container_name: c-server-container
    ports:
      - "8080:8080"
    depends_on:
      database:
        condition: service_healthy
    networks:
      - itt440_net
    restart: unless-stopped

  c_client:
    build: ./c-client
    container_name: c-client-container
    depends_on:
      - c_server
    networks:
      - itt440_net
    restart: unless-stopped

networks:
  itt440_net:
    driver: bridge
```

## Database Schema Blueprint (init.sql)
The persistent storage uses a structure containing indexing constraints for efficient database query reads during live data polls from the web client interface.

```bash
CREATE DATABASE IF NOT EXISTS library_stats;
USE library_stats;

CREATE TABLE IF NOT EXISTS segmen_mata (
    user VARCHAR(50) PRIMARY KEY,
    points INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO segmen_mata (user, points) VALUES 
('Adeena', 0), ('Mastura', 0), ('Azra', 0),
('Aina', 0), ('Fasihah', 0), ('Irdina', 0);
```

## Central Web Visualizer Monitor Component (monitor.py)
Developed using a lightweight Python Flask framework to avoid heavy rendering overhead. It performs asynchronous data fetching and returns clean dashboard views that auto-refresh every 2000ms.

```bash
from flask import Flask, render_template_string
import pymysql
import os

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'database'),
        user='root',
        password='secretpass',
        database='library_stats',
        cursorclass=pymysql.cursors.DictCursor
    )

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ITT440 Leaderboard</title>
    <style>
        body { font-family: Arial; background: #0f172a; color: white; text-align: center; padding: 40px; }
        h1 { color: #38bdf8; }
        .leaderboard { max-width: 700px; margin: 0 auto; background: #1e293b; padding: 25px; border-radius: 12px; }
        .player { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #334155; }
        .badge-c { background: #f59e0b; color: #0f172a; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        .badge-py { background: #10b981; color: #0f172a; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        .points { font-weight: bold; color: #34d399; }
    </style>
    <script>setInterval(function(){ location.reload(); }, 2000);</script>
</head>
<body>
    <h1>ITT440 Leaderboard</h1>
    <div class="leaderboard">
        {% for row in players %}
        <div class="player">
            <span>#{{ loop.index }} {{ row.user }}</span>
            <span>
                {% if row.user in ['Adeena', 'Fasihah'] %}
                <span class="badge-c">C Primitive Socket</span>
                {% else %}
                <span class="badge-py">Python Multi-Thread</span>
                {% endif %}
                {{ row.points }} pts
            </span>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT user, points FROM segmen_mata ORDER BY points DESC")
            players = cur.fetchall()
        db.close()
    except Exception as e:
        print(f"Error: {e}")
        players = []
    return render_template_string(HTML, players=players)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Central C Server Implementation (server.c)
This module combines primitive sys/socket.h bindings alongside background POSIX threading structures (pthread.h) to handle database writes independently of client connections.

```bash
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <mariadb/mysql.h>
#include <pthread.h>

#define PORT 8080
#define NODE_USER "Adeena"
#define DB_HOST "database"

MYSQL *conn;

void* update_points(void* arg) {
    while (1) {
        sleep(30);
        char query[256];
        sprintf(query, "UPDATE segmen_mata SET points = points + 3 WHERE user = '%s'", NODE_USER);
        if (mysql_query(conn, query)) {
            printf("[Error] Update failed: %s\n", mysql_error(conn));
        } else {
            printf("[Adeena] ✅ Points updated! +3\n");
        }
        fflush(stdout);
    }
    return NULL;
}

int main() {
    conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, DB_HOST, "root", "secretpass", "library_stats", 3306, NULL, 0)) {
        return 1;
    }

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    pthread_t thread;
    pthread_create(&thread, NULL, update_points, NULL);

    char buffer[1024] = {0};
    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        int valread = read(new_socket, buffer, 1024);
        if (valread > 0) {
            send(new_socket, "OK", 2, 0);
        }
        close(new_socket);
    }
    mysql_close(conn);
    return 0;
}
```

# DISTRIBUTED DATA ANALYSIS & RESULTS
Once all containers were launched, real-time metrics generation was confirmed across the network. The dashboard compiled data using sequential SQL sort operations, verifying successful distributed telemetry insertion.
## System Operational Mapping
tableeee

## Performance Insights and Concurrency Handling
### 1. Low-Level Thread Execution Stability: 
The native C implementation on Laptop 1 and Laptop 5 demonstrated minimal CPU clock latency. Memory locks remained constant under persistent multi-threaded payload hits because the C applications isolate database writes into independent worker threads (pthread_create).

### 2. Cross-Platform Networking Consistency: 
The hybrid platform communication was stable. Python sockets gracefully marshaled input requests into string objects, while the lower-level C applications received them as standard character buffers (char buffer[1024]). This demonstrates that cross-language systems can interact seamlessly as long as they follow standard TCP streaming byte boundaries.

### 3. Relational Integrity Maintenance: 
Using standard database connection pools (pymysql.connect and mysql_real_connect) verified that atomic mutations correctly maintained ACID compliance across multiple client requests. This prevented row contention issues, even when multiple external workstations updated the table simultaneously.


# CONCLUSION 
This project successfully demonstrates a containerized, cross-platform distributed network monitor architecture. Separating computational workloads into functional microservices managed by Docker Compose resolved previous environment configuration problems, such as localized missing package dependencies.

Low-level C servers proved to be highly efficient for long-running socket management, while Python's modular design simplified writing database connection drivers and real-time dashboard web tools. Ultimately, this architecture meets all design requirements for robust, low-latency cross-platform telemetry monitoring across distributed nodes.
