

# 🚀 Fast Log Analyzer: Using Parallel Computing to Detect Security Threats

**Course Code: ITT440: Network Programming**

**Lecturer :  Shahadan Bin Saad**

**Youtube Link : https://youtu.be/6e2JYMypeDA?si=Sz6S3xXJdR5DSBXB**

**Github Link : https://github.com/FaezBun/kelasirlog**

# 🛡️1. Mission Objective
In modern cybersecurity, Speed = Survival. Processing 15 million lines of logs using traditional, single-core methods is a bottleneck that leaves systems vulnerable.

The Fast Log Analyzer is a high-performance engine that utilizes Parallel Computing to shred through massive datasets. By distributing the workload across all available CPU threads, it transforms an ordinary laptop into a forensic powerhouse, detecting over 1.2 million threats in a fraction of the time.


# 💻 2. Hardware & Environment

1. Processor: Quad-Core / Octa-Core CPU

2. Memory: 8GB RAM minimum 

3. OS: Linux Environment (Ubuntu 22.04+ recommended).

4. Runtime: Python 3.8+ with matplotlib for analytics and tqdm for real-time progress.

# Disclaimer 

Please note that the **15,000,000 line log file** (`15mil_server_forensic.log`) is **not included** in this GitHub repository.

# 🛠️ 3. Deployment Guide
## A. System Ignition


###  Create a new project folder

```bash
mkdir ITT440_LogAnalyzer
 cd ITT440_LogAnalyzer
```

### Initialize a virtual environment in the 'venv' directory

```bash
python3 -m venv venv
```

### Standard activation command for Linux/macOS

```bash
source venv/bin/activate
```

### Install tqdm (Real-time progress bars)

```bash
pip install tqdm
```

### Install Matplotlib (Automatic performance graph generation)

```bash
pip install matplotlib
```

## B.  Engagement Protocol
To launch the analysis, execute the main engine:


### Activate Venv

```bash
source venv/bin/activate
```

### Run Program 

```bash
python3 analyzer.py
```


# 📊 4. Battlefield Analytics 

## A. 15 Million Lines of Log
When the analyzer completes its scan, it generates a comprehensive Forensic Breakdown. Here is what a typical high-stress test looks like:


| Security Event             | Detection Count |
|----------------------------|----------------|
| SQL_INJECTION_DETECTED     | 256,278 cases  |
| BRUTE_FORCE_ATTEMPT        | 254,861 cases  |
| XSS_ATTACK_DETECTED        | 254,861 cases  |
| PATH_TRAVERSAL_ATTACK      | 172,471 cases  |
| UNAUTHORIZED_ADMIN_ACCESS  | 172,471 cases  |
| **Total Critical Threats** | **1,110,942**  |


![15mil](https://raw.githubusercontent.com/FaezBun/kelasirlog/refs/heads/main/real15milss.png)

### Performance Benchmark


1. Concurrent : 2.8792 Seconds

2. Parallel (8 Cores): 11.34 Seconds

3. Sequential (1 Core): 36.14 Seconds

4. Performance Gain: 🚀 3.19x Faster

![15mil](https://raw.githubusercontent.com/FaezBun/kelasirlog/refs/heads/main/real15mil.png)


## B.100K Lines Of Log


| Security Event          | Detection Count |
|-------------------------|-----------------|
| SQL_INJECTION_DETECTED     | 4 568 cases  |
| BRUTE_FORCE_ATTEMPT        | 4,568 cases  |
| XSS_ATTACK_DETECTED        | 4,568 cases  |
| PATH_TRAVERSAL_ATTACK      | 2,284 cases  |
| UNAUTHORIZED_ADMIN_ACCESS  | 2,284 cases  |
| **Total Critical Threats** | **18,272**   |


![100K](https://raw.githubusercontent.com/FaezBun/kelasirlog/refs/heads/main/real100kss.png)

### Performance Benchmark


1. Concurrent : 0.0306 Seconds

2. Parallel (8 Cores): 0.11 Seconds

3. Sequential (1 Core): 0.30 Seconds

4. Performance Gain: 🚀 2.58x Faster

![100k](https://raw.githubusercontent.com/FaezBun/kelasirlog/refs/heads/main/real100k.png)




# 🧠 5. How It Works (The Logic)
The engine doesn't just work harder; it works smarter by using a MapReduce Pattern.


1. Partition (Map): The 15 million lines are sliced into 8 equal chunks.

2. Analyze: Each CPU core receives a chunk and runs high-speed Regex matching simultaneously.

3. Synthesize (Reduce): The engine pulls the results from all cores together to produce the final forensic tally.

# 🏁 7. Final Verdict
The Fast Log Analyzer proves that **parallel computing** is the gold standard for modern forensics. 

By cutting analysis time by over 70%, we ensure that network administrators can respond to breaches in real-time rather than hours after the damage is done.


# Status: Mission Accomplished. System Optimized. 🚀 



