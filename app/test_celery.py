import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.tasks import (
        run_periodic_analytics_task,
        generate_load_reports_all_zones_task,
        check_overload_all_zones_task
    )
except ImportError:
    from tasks import (
        run_periodic_analytics_task,
        generate_load_reports_all_zones_task,
        check_overload_all_zones_task
    )

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
        
    print("\nSending load report generation task to queue...")
    try:
        result_load = generate_load_reports_all_zones_task.delay()
        print(f"✅ Load report generation task sent! Task ID: {result_load.id}")
    except Exception as e:
        print(f"❌ Failed to dispatch load report generation task: {e}")

    print("\nSending overload checks task to queue...")
    try:
        result_overload = check_overload_all_zones_task.delay()
        print(f"✅ Overload checks task sent! Task ID: {result_overload.id}")
    except Exception as e:
        print(f"❌ Failed to dispatch overload checks task: {e}")
        
    print("\nWait for Celery worker process logs to see execution details.")
    print("=" * 60)

if __name__ == "__main__":
    trigger_task()
