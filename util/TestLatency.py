def test_latency(handler, stream):
    
    # Perform your stream processing here
    
    
    latency = handler.time
    print(f"Latency for stream {stream}: {latency} seconds")

if __name__ == "__main__":
    # Example usage
    test_latency("Stream 1")
    test_latency("Stream 2")
    test_latency("Stream 3")