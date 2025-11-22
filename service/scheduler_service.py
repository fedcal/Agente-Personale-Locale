from datetime import datetime
from typing import Callable, Dict

from apscheduler.schedulers.background import BackgroundScheduler
from utils.logger import get_logger

log = get_logger(__name__)


class SchedulerService:
    """
    Wrapper leggero su APScheduler per programmare task.
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs: Dict[str, str] = {}
        self.started = False

    def start(self):
        if not self.started:
            self.scheduler.start()
            self.started = True
            log.info("Scheduler avviato")

    def add_interval_job(self, name: str, func: Callable, seconds: int):
        job = self.scheduler.add_job(func, "interval", seconds=seconds, id=name, next_run_time=datetime.now())
        self.jobs[name] = job.id
        self.start()

    def remove_job(self, name: str):
        job_id = self.jobs.get(name)
        if job_id:
            self.scheduler.remove_job(job_id)
            self.jobs.pop(name, None)
