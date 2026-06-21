import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.redis_client import (
        get_redis_connection,
        cache_analytics_results,
        get_cached_analytics,
        store_latest_meter_reading,
        get_latest_meter_reading,
        clear_all_cache
    )
except ImportError:
    from redis_client import (
        get_redis_connection,
        cache_analytics_results,
        get_cached_analytics,
        store_latest_meter_reading,
        get_latest_meter_reading,
        clear_all_cache
    )

def run_tests():
    print("=" * 60)
    print("        REDIS CLIENT INTEGRATION VERIFICATION TESTS        ")
    print("=" * 60)

    print("\n[Test 1] Verifying connectivity to Redis server...")
    try:
        client = get_redis_connection()
        ping_response = client.ping()
        print(f"✅ Redis Ping Result: {ping_response} (Connection Successful)")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("Ensure that redis-server is running on localhost:6379 before running tests.")
        sys.exit(1)

    print("\n[Test 2] Clearing current database keys for clean test state...")
    if clear_all_cache():
        print("✅ Database successfully flushed.")
    else:
        print("❌ Database flush failed.")

    print("\n[Test 3] Testing analytics caching and serialization/deserialization...")
    test_key = "test:analytics:data"
    test_data = {
        "report_type": "daily_summary",
        "total_consumption_kwh": 352.45,
        "active_meters": ["METER_001", "METER_002", "METER_003"],
        "calculated_at": "2026-06-19 23:00:00"
    }
    
    cache_success = cache_analytics_results(test_key, test_data, ttl=5)
    if cache_success:
        print(f"✅ Successfully cached test payload under key '{test_key}'.")
    else:
        print(f"❌ Failed to cache test payload.")
        
    retrieved_data = get_cached_analytics(test_key)
    if retrieved_data == test_data:
        print(f"✅ Cache Hit: Successfully retrieved and deserialized cache data.")
        print(f"   Payload: {retrieved_data}")
    else:
        print(f"❌ Cache Retrieve Failed: Retrieved {retrieved_data}")

    print("Waiting 6 seconds for cache TTL expiration...")
    time.sleep(6)
    expired_data = get_cached_analytics(test_key)
    if expired_data is None:
        print("✅ Cache Expiration: Cached data successfully expired and removed.")
    else:
        print(f"❌ Cache Expiration Failed: Key still exists: {expired_data}")

    print("\n[Test 4] Testing smart meter latest readings (Redis Hashes)...")
    meter_id = "TEST_METER_999"
    
    t1 = "2026-06-19 12:00:00"
    load1 = 4.25
    store_latest_meter_reading(meter_id, t1, load1)
    reading1 = get_latest_meter_reading(meter_id)
    
    if reading1 and reading1["timestamp"] == t1 and reading1["consumption_kw"] == load1:
        print(f"✅ Successfully stored and retrieved first reading: {reading1}")
    else:
        print(f"❌ Failed to store/retrieve first reading: {reading1}")

    t2 = "2026-06-19 12:30:00"
    load2 = 5.80
    store_latest_meter_reading(meter_id, t2, load2)
    reading2 = get_latest_meter_reading(meter_id)
    
    if reading2 and reading2["timestamp"] == t2 and reading2["consumption_kw"] == load2:
        print(f"✅ Successfully updated to newer reading: {reading2}")
    else:
        print(f"❌ Failed to update to newer reading: {reading2}")

    t_old = "2026-06-19 11:45:00"
    load_old = 1.10
    updated = store_latest_meter_reading(meter_id, t_old, load_old)
    reading3 = get_latest_meter_reading(meter_id)
    
    if not updated and reading3["timestamp"] == t2:
        print("✅ Out-of-order updates prevention: Ignored older reading timestamp.")
        print(f"   Current Redis Reading remains the latest: {reading3}")
    else:
        print(f"❌ Out-of-order update protection failed! Data in Redis: {reading3}")

    print("=" * 60)
    print("                 ALL REDIS TESTS COMPLETED                 ")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
