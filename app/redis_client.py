import json
import redis
from typing import Any, Dict, Optional

_redis_pool: Optional[redis.ConnectionPool] = None

def get_redis_connection(host: str = "localhost", port: int = 6379, db: int = 0) -> redis.Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_timeout=5.0
        )
    return redis.Redis(connection_pool=_redis_pool)

def cache_analytics_results(key: str, data: Any, ttl: int = 3600) -> bool:
    try:
        client = get_redis_connection()
        serialized_data = json.dumps(data)
        return bool(client.set(key, serialized_data, ex=ttl))
    except redis.RedisError as e:
        print(f"[Redis Cache Error] Failed to cache analytics results for key '{key}': {e}")
        return False

def get_cached_analytics(key: str) -> Optional[Any]:
    try:
        client = get_redis_connection()
        cached_data = client.get(key)
        if cached_data:
            return json.loads(cached_data)
    except redis.RedisError as e:
        print(f"[Redis Cache Error] Failed to retrieve cached data for key '{key}': {e}")
    return None

def store_latest_meter_reading(meter_id: str, timestamp: str, consumption_kw: float) -> bool:
    try:
        client = get_redis_connection()
        hash_key = f"meter:latest:{meter_id}"
        
        existing_timestamp = client.hget(hash_key, "timestamp")
        if existing_timestamp and timestamp < existing_timestamp:
            return False
            
        client.hset(hash_key, mapping={
            "timestamp": timestamp,
            "consumption_kw": str(consumption_kw)
        })
        return True
    except redis.RedisError as e:
        print(f"[Redis Client Error] Failed to store latest reading for meter '{meter_id}': {e}")
        return False

def get_latest_meter_reading(meter_id: str) -> Optional[Dict[str, Any]]:
    try:
        client = get_redis_connection()
        hash_key = f"meter:latest:{meter_id}"
        
        data = client.hgetall(hash_key)
        if data:
            data["consumption_kw"] = float(data["consumption_kw"])
            return data
    except redis.RedisError as e:
        print(f"[Redis Client Error] Failed to retrieve reading for meter '{meter_id}': {e}")
    return None

def clear_all_cache() -> bool:
    try:
        client = get_redis_connection()
        client.flushdb()
        return True
    except redis.RedisError as e:
        print(f"[Redis Admin Error] Failed to flush database: {e}")
        return False
