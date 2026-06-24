import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app.tasks import run_periodic_analytics_task
except ImportError:
    from tasks import run_periodic_analytics_task

def trigger_task():
    print("=" * 60)
    print("           CELERY ASYNCHRONOUS TASK VERIFICATION           ")
    print("=" * 60)
    
    print("Sending task to Celery queue...")
    try:
        result = run_periodic_analytics_task.delay()
        print(f"✅ Task sent successfully! Task ID: {result.id}")
        print("Status:", result.status)
        print("Wait for Celery worker process logs to see the task execution.")
    except Exception as e:
        print(f"❌ Failed to dispatch Celery task: {e}")
        print("Make sure Redis is running on localhost:6379")
        
    print("=" * 60)

if __name__ == "__main__":
    trigger_task()
