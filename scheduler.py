import schedule
import time
import threading
from typing import Callable

class Scheduler:
    """
    Handles periodic scheduling using the schedule module.
    """

    def __init__(self, interval_minutes: int, job_func: Callable):
        self.interval_minutes = interval_minutes
        self.job_func = job_func

    def start(self):
        """
        Start the recurring job every interval_minutes.
        """

        schedule.every(self.interval_minutes).minutes.do(self.job_func)

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        print(f"Scheduler started: job scheduled every {self.interval_minutes} minutes.")
