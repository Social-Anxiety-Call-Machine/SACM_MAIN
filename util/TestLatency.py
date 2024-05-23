import time

def test_latency(stream):
    start_time = time.time()
    # Perform your stream processing here
    # ...
    end_time = time.time()
    latency = end_time - start_time
    print(f"Latency for stream {stream}: {latency} seconds")

# Example usage
test_latency("Stream 1")
test_latency("Stream 2")
test_latency("Stream 3")