import time
from celery import shared_task


@shared_task
def test_task(message):
    time.sleep(5)
    print(f"Task completed! Message was: {message}")
    return f"Processed: {message}"