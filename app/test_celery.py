import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.tasks import run_periodic_analytics_task, monitor_all_zones_task
except ImportError:
    from tasks import run_periodic_analytics_task, monitor_all_zones_task

def trigger_task():
    print("=" * 60)
    print("           CELERY ASYNCHRONOUS TASK VERIFICATION           ")
    print("=" * 60)
    
    print("Sending CSV analytics task to queue...")
    try:
        result_analytics = run_periodic_analytics_task.delay()
        print(f"✅ CSV analytics task sent! Task ID: {result_analytics.id}")
    except Exception as e:
        print(f"❌ Failed to dispatch CSV analytics task: {e}")
        
    print("\nSending database zones monitoring task to queue...")
    try:
        result_monitor = monitor_all_zones_task.delay()
        print(f"✅ Database monitoring task sent! Task ID: {result_monitor.id}")
    except Exception as e:
        print(f"❌ Failed to dispatch database monitoring task: {e}")
        
    print("\nWait for Celery worker process logs to see execution details.")
    print("=" * 60)

if __name__ == "__main__":
    trigger_task()
