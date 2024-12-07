import time
import matplotlib.pyplot as plt
from herd_python import HerdClient

# Initialize the Herd client
herd = HerdClient(port=7878)

# Function to measure latency
def measure_latency(operation, key, value=None):
    start_time = time.time()  # Record start time
    if operation == "set":
        herd.set(key, value)  # Perform the write operation
    elif operation == "get":
        herd.get(key)  # Perform the read operation
    else:
        raise ValueError("Invalid operation. Use 'set' or 'get'.")
    end_time = time.time()  # Record end time
    latency = (end_time - start_time) * 1000  # Convert to milliseconds
    return time.time(), latency  # Return timestamp and latency

# Collect latency data
latency_data = []
num_operations = 100  # Number of operations to perform

for i in range(num_operations):
    operation_type = "get" if i % 2 == 0 else "set"  # Alternate between get and set
    timestamp, latency = measure_latency(operation_type, str(i), "Test Value")
    latency_data.append((timestamp, latency))

# Save data for graphing
timestamps, latencies = zip(*latency_data)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(timestamps, latencies, marker='o', linestyle='-', color='b', label="Latency (ms)")

# Customize the graph
plt.title("Operation Latency Over Time")
plt.xlabel("Timestamp (s)")
plt.ylabel("Latency (ms)")
plt.grid(True)
plt.legend()

# Show the graph
plt.show()