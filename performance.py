import time

def run_performance_test(db):
    results = []

    # Query WITHOUT index
    start = time.time()
    list(db.readings.find({"deviceId": {"$exists": True}}))
    no_index_time = time.time() - start

    results.append({
        "Test": "Query without index",
        "Execution Time (s)": round(no_index_time, 5)
    })

    # Create index
    db.readings.create_index("deviceId")

    # Query WITH index
    start = time.time()
    list(db.readings.find({"deviceId": {"$exists": True}}))
    index_time = time.time() - start

    results.append({
        "Test": "Query with index",
        "Execution Time (s)": round(index_time, 5)
    })

    # Cleanup (optional but good practice)
    db.readings.drop_index("deviceId_1")

    return results
