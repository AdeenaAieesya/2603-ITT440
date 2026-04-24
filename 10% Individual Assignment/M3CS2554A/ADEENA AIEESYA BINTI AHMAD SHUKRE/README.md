# Airport Baggage Handling and Sorting Simulator

**NAME:** ADEENA AIEESYA BINTI AHMAD SHUKRE

**STUDENT ID:** 2024648084

**CLASS:** M3CS2554A

**COURSE CODE:** ITT440 Network Programming

-------------------------------------------------------------------------------------------


## PROBLEM STATEMENT
In the context of airport baggage handling, where thousands or even millions of records may need to be processed, selecting the most efficient processing method becomes critical.

While the sequential processing provides a simple approach, it may not be suitable for handling large volumes of data efficiently. To overcome this issue, concurrency and parallelism are introduced in modern computing. Concurrent programming allows several tasks to be managed at once, improving system responsiveness, while parallel programming allows tasks to be executed simultaneously across various CPU cores, improving performance for computationally demanding workloads.

Thus, this project focuses on evaluating and comparing three processing techniques, which are sequential, concurrent, and parallel processing by simulating a large scale airport baggage handling system. The aim is to identify which approach provides better performance and scalability when handling large datasets.


## SYSTEM DESIGN
First, the system generates baggage data automatically based on user input. Each baggage record contain basic information such as bag ID, weight, destination, priority, and complexity level. The use of automatically generated data allows the system to simulate large scale situations without requiring manual input.

Next, the system processes the generated data using three different techniques. In sequential processing, each baggage record is processed one by one. In concurrent processing, multiple threads are used to process baggage records simultaneously by retrieving tasks from a shared queue. In parallel processing, multiple processes are created using a process pool, where each process handles part of the workload independently.

The system measures the execution time for each processing method using a timer. This allows a direct comparison of performance between the three approaches. After processing is complete, the system displays a summary of results, including the number of baggage items processed and the total workload score.


## SYSTEM REQUIREMENTS
To run the Airport Baggage Handling and Sorting Simulator, the system requirements needed are : 
- Operating System : Windows, Linux (Kali), or macOS
- Python Version : Python 3.8 or above
- Processor : Multicore CPU
- RAM : Minimum 4GB, but the bigger the better as the dataset that will be handled are massive.
- Storage : At least 1GB free space
- Terminal : Required to run the program


## INSTALLATION STEPS

***A. LAUNCH THE SIMULATOR***
**Navigate to project folder**

```bash
cd airport_baggage_sim
```

**Run the program**

```bash
python3 airport_main.py
```

***B. PROVIDE DESIRED INPUT***
**When prompted, enter the required values, for example:**

```bash
Enter number of baggage records (example: 1000000): 100000
Enter number of threads: 4
Enter number of processes: 4
```

***C. SYSTEM EXECUTION***
**The program will automatically:**

```bash
- Generate baggage data
- Execute sequential processing
- Execute concurrent processing (threading)
- Execute parallel processing (multiprocessing)
- Display execution time and performance comparison
```



## SAMPLE OUTPUT

```bash
===== AIRPORT BAGGAGE HANDLING SIMULATOR =====

Generating baggage data...
100000 baggage records generated.

Running sequential processing...
Sequential completed in 8.5000 seconds

Running threading processing...
Threading completed in 6.9000 seconds

Running multiprocessing processing...
Multiprocessing completed in 3.2000 seconds

========== PERFORMANCE COMPARISON ==========
Sequential      : 8.5000 seconds
Threading       : 6.9000 seconds
Multiprocessing : 3.2000 seconds
Fastest Method: Multiprocessing
```


## ANALYTIC
| Destination               | Number of Bag  | 
|---------------------------|----------------| 
| KUL                       | 4 568 bags    | 
| JHB                       | 4,568 bags    | 
| PEN                       | 4,568 bags    | 
| LGK                       | 2,284 bags    | 
| BKI                       | 2,284 bags    | 
| KCH                       | 2,284 bags    |
| **Total Processing Load** | **18,272**     |




## CONCLUSION
In conclusion, this project successfully developed an airport baggage handling and sorting simulator using Python to process large scale data efficiently. The system implemented three different processing techniques, which are sequential processing, concurrent processing using threading, and parallel processing using multiprocessing, to simulate real world scenarios when a huge amount of baggage records must be handled. The results demonstrated that sequential processing, although simple, becomes inefficient as the dataset size increases due to its one by one execution approach. Threading provided some improvement by allowing tasks to be handled concurrently, but its performance remained limited for CPU intensive operations.

On the other hand, multiprocessing achieved the best performance among all techniques by utilizing multiple CPU cores, enabling true parallel execution and significantly reducing processing time for large datasets. This shows that parallel processing is the most suitable approach for handling large-scale and computationally intensive tasks such as airport baggage handling systems. Overall, the project highlights the importance of selecting the appropriate processing method based on the nature of the workload and demonstrates how concurrency and parallelism can improve efficiency and scalability in practical applications.



------------------------------------------------------------------------------------------------

## SOURCE CODE
import random
import time
import threading
import multiprocessing as mp
from queue import Queue

# =========================================================
# AIRPORT BAGGAGE HANDLING AND SORTING SIMULATOR
# ---------------------------------------------------------
# This program demonstrates:
# 1. Sequential processing
# 2. Concurrent processing using threading
# 3. Parallel processing using multiprocessing
#
# =========================================================

# Predefined destinations and priorities
DESTINATIONS = ["KUL", "JHB", "PEN", "LGK", "BKI", "KCH"]
PRIORITIES = ["Normal", "Priority", "Fragile"]


# ---------------------------------------------------------
# DATA GENERATION
# ---------------------------------------------------------
def generate_baggage_data(num_bags):
    """
    Generate baggage records automatically.

    Each baggage is stored as a tuple:
    (bag_id, weight, destination_index, priority_index, complexity)

    Tuples are used to reduce memory usage for very large datasets.
    """
    baggage_list = []

    for i in range(1, num_bags + 1):
        bag = (
            i,  # bag ID
            random.randint(5, 30),  # weight in kg
            random.randint(0, len(DESTINATIONS) - 1),  # destination index
            random.randint(0, len(PRIORITIES) - 1),  # priority index
            random.randint(2000, 6000)  # workload size
        )
        baggage_list.append(bag)

    return baggage_list


# ---------------------------------------------------------
# CPU WORKLOAD SIMULATION
# ---------------------------------------------------------
def sorting_workload(bag):
    """
    Simulate CPU-intensive baggage sorting.

    This creates artificial workload so we can compare:
    - sequential
    - threading
    - multiprocessing
    """
    bag_id, weight, destination_index, priority_index, complexity = bag
    result = 0

    # CPU-heavy loop
    for i in range(complexity):
        result += (i * i) % 97

    # Return minimal result to save memory
    return destination_index, result


# ---------------------------------------------------------
# SEQUENTIAL PROCESSING
# ---------------------------------------------------------
def process_sequential(baggage_list):
    """
    Sequential processing:
    Processes each baggage one by one.
    """
    start_time = time.perf_counter()

    destination_count = [0] * len(DESTINATIONS)
    total_score = 0

    for bag in baggage_list:
        destination_index, score = sorting_workload(bag)
        destination_count[destination_index] += 1
        total_score += score

    end_time = time.perf_counter()
    return destination_count, total_score, end_time - start_time


# ---------------------------------------------------------
# THREAD WORKER FUNCTION
# ---------------------------------------------------------
def thread_worker(task_queue, destination_count, total_score_box, lock):
    """
    Worker function for threading.

    Each thread:
    - takes tasks from the queue
    - processes them
    - updates shared results using a lock
    """
    while True:
        try:
            bag = task_queue.get_nowait()
        except:
            break

        destination_index, score = sorting_workload(bag)

        # Lock makes shared updates safe
        with lock:
            destination_count[destination_index] += 1
            total_score_box[0] += score

        task_queue.task_done()


# ---------------------------------------------------------
# CONCURRENT PROCESSING USING THREADING
# ---------------------------------------------------------
def process_threading(baggage_list, num_threads=4):
    """
    Concurrent processing using threading.

    Threads simulate multiple baggage counters handling tasks.
    """
    start_time = time.perf_counter()

    task_queue = Queue()
    destination_count = [0] * len(DESTINATIONS)

    # Use a list so threads can update one shared total score
    total_score_box = [0]

    lock = threading.Lock()
    threads = []

    # Put all baggage into queue
    for bag in baggage_list:
        task_queue.put(bag)

    # Create and start threads
    for _ in range(num_threads):
        t = threading.Thread(
            target=thread_worker,
            args=(task_queue, destination_count, total_score_box, lock)
        )
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end_time = time.perf_counter()
    return destination_count, total_score_box[0], end_time - start_time


# ---------------------------------------------------------
# PARALLEL PROCESSING USING MULTIPROCESSING
# ---------------------------------------------------------
def process_multiprocessing(baggage_list, num_processes=4):
    """
    Parallel processing using multiprocessing.

    Multiple processes run on multiple CPU cores.
    """
    start_time = time.perf_counter()

    destination_count = [0] * len(DESTINATIONS)
    total_score = 0

    # Pool creates worker processes
    with mp.Pool(processes=num_processes) as pool:
        # chunksize helps performance for large datasets
        for destination_index, score in pool.map(
            sorting_workload,
            baggage_list,
            chunksize=1000
        ):
            destination_count[destination_index] += 1
            total_score += score

    end_time = time.perf_counter()
    return destination_count, total_score, end_time - start_time


# ---------------------------------------------------------
# SUMMARY OUTPUT
# ---------------------------------------------------------
def print_summary(destination_count, total_score):
    """
    Print summary instead of full data.
    This is important for large datasets.
    """
    print("\nBaggage summary by destination:")
    for i, count in enumerate(destination_count):
        print(f"{DESTINATIONS[i]}: {count} bags")

    print(f"Total sort score: {total_score}")


# ---------------------------------------------------------
# PERFORMANCE COMPARISON
# ---------------------------------------------------------
def compare_times(seq_time, thread_time, process_time):
    """
    Compare execution times of all three methods.
    """
    print("\n========== PERFORMANCE COMPARISON ==========")
    print(f"Sequential      : {seq_time:.4f} seconds")
    print(f"Threading       : {thread_time:.4f} seconds")
    print(f"Multiprocessing : {process_time:.4f} seconds")

    fastest = min(seq_time, thread_time, process_time)

    if fastest == seq_time:
        print("Fastest Method: Sequential")
    elif fastest == thread_time:
        print("Fastest Method: Threading")
    else:
        print("Fastest Method: Multiprocessing")


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------
def main():
    print("===== AIRPORT BAGGAGE HANDLING SIMULATOR =====")

    try:
        # User enters only the number of data to generate
        num_bags = int(input("Enter number of baggage records (example: 1000000): "))
        num_threads = int(input("Enter number of threads: "))
        num_processes = int(input("Enter number of processes: "))
    except ValueError:
        print("Invalid input.")
        return

    # Automatically generate data
    print("\nGenerating baggage data...")
    baggage_data = generate_baggage_data(num_bags)
    print(f"{num_bags} baggage records generated.")

    # Run sequential version
    print("\nRunning sequential processing...")
    seq_dest, seq_score, seq_time = process_sequential(baggage_data)
    print(f"Sequential completed in {seq_time:.4f} seconds")

    # Run threading version
    print("\nRunning threading processing...")
    thread_dest, thread_score, thread_time = process_threading(
        baggage_data, num_threads
    )
    print(f"Threading completed in {thread_time:.4f} seconds")

    # Run multiprocessing version
    print("\nRunning multiprocessing processing...")
    process_dest, process_score, process_time = process_multiprocessing(
        baggage_data, num_processes
    )
    print(f"Multiprocessing completed in {process_time:.4f} seconds")

    # Print summary
    print_summary(process_dest, process_score)

    # Compare times
    compare_times(seq_time, thread_time, process_time)


# Required for multiprocessing
if __name__ == "__main__":
    main()

