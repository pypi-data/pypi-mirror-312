import asyncio
from typing import List
from datetime import datetime
from moirai_engine.core.job import Job


class Engine:
    def __init__(self, max_workers=4, listener: callable = None):
        self.job_queue = asyncio.Queue()
        self.is_running = False
        self.max_workers = max_workers
        self.tasks: List[asyncio.Task] = []
        self.notification_listeners: dict[str, List[callable]] = {"_moirai": []}

        if listener:
            self.notification_listeners["_moirai"].append(listener)

    async def start(self):
        if not self.is_running:
            self.is_running = True
            for _ in range(self.max_workers):
                t = asyncio.create_task(self.worker())
                self.tasks.append(t)
            self.notify("[Start] Engine")

    async def stop(self):
        if self.is_running:
            self.is_running = False
            await self.job_queue.join()
            for t in self.tasks:
                t.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)
            self.notify("[Stop] Engine")

    async def worker(self):
        while self.is_running:
            if self.job_queue.empty():
                await asyncio.sleep(1)
                continue
            job = await self.job_queue.get()
            try:
                await job.run()
            except Exception as e:
                print(f"Error in job {job.label}: {str(e)}")
                self.notify(f"[Error] job_id:{job.label}.  err:{str(e)}")
            finally:
                self.job_queue.task_done()

    async def add_job(self, job: Job, listener: callable = None):
        job.engine = self
        if listener:
            if job.id not in self.notification_listeners:
                self.notification_listeners[job.id] = []
            self.notification_listeners[job.id].append(
                listener
            )  # This may  cause duplicate listeners
        await self.job_queue.put(job)
        self.notify(f"[Queued] {job.label}")

    def add_listener(self, listener: callable, job_id: str = "_moirai"):
        """Add a new listener to job_id. If job_id not defined, read engine notifications"""
        if job_id not in self.notification_listeners:
            self.notification_listeners[job_id] = []
        self.notification_listeners[job_id].append(listener)

    def notify(self, message: str, job_id: str = "_moirai"):
        if job_id not in self.notification_listeners:
            self.notification_listeners[job_id] = []
        for listener in self.notification_listeners[job_id]:
            asyncio.ensure_future(listener(message))

    # async def notify(self, message: str, job_id: str = ""):
    #     print(f"Job {job_id}: {message}")

    # async def run(self):
    #     while self.is_running:
    #         try:
    #             job = await self.job_queue.get()
    #             if job:
    #                 # self.job_notification_queues[job.id] = asyncio.Queue()
    #                 # self.job_histories[job.id] = []
    #                 job.engine = self  # Set the engine reference
    #                 asyncio.create_task(self.process_job(job))
    #                 await self.notify(f"Job {job.label} started", job.id)
    #         except asyncio.QueueEmpty:
    #             await asyncio.sleep(1)

    # async def process_job(self, job: Job):
    #     """
    #     Processes a single job.

    #     Args:
    #         job (Job): The job to be processed.
    #     """
    #     try:
    #         await job.run()
    #         await self.notify(f"Job {job.label} completed", job.id)
    #     except Exception as e:
    #         await self.notify(f"Job {job.label} failed: {str(e)}", job.id)

    # async def add_job(self, job: Job):
    #     """
    #     Adds a job to the job queue.

    #     Args:
    #         job (Job): The job to be added.
    #     """
    #     await self.job_queue.put(job)
    #     await self.notify(f"Job added: {job.label}", job.id)

    # async def notify(self, message: str, job_id: str = None):
    #     """
    #     Sends a notification message.

    #     Args:
    #         message (str): The notification message.
    #         job_id (str, optional): The ID of the job associated with the notification.
    #     """
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     notification = {"job_id": job_id, "message": message, "timestamp": timestamp}
    #     if job_id and job_id in self.job_notification_queues:
    #         await self.job_notification_queues[job_id].put(notification)
    #         self.job_histories[job_id].append(notification)
    #         for listener in self.notification_listeners:
    #             if asyncio.iscoroutinefunction(listener):
    #                 await listener(notification)
    #             else:
    #                 listener(notification)
    #     else:
    #         ...
    #         # print(notification)  # Fallback to console if no job_id is provided

    # async def get_notifications(self, job_id: str):
    #     notifications = []
    #     if job_id in self.job_notification_queues:
    #         while not self.job_notification_queues[job_id].empty():
    #             notifications.append(await self.job_notification_queues[job_id].get())
    #     return notifications

    # def add_notification_listener(self, listener):
    #     if asyncio.iscoroutinefunction(listener):
    #         self.notification_listeners.append(listener)
    #     else:
    #         raise ValueError("Listener must be an async function")

    # async def start_notification_listener(self, job_id: str):
    #     while self.is_running:
    #         notifications = await self.get_notifications(job_id)
    #         for notification in notifications:
    #             print(notification)
    #         await asyncio.sleep(1)  # Adjust the sleep time as needed

    # async def get_notification_history(self, job_id: str):
    #     if job_id in self.job_histories:
    #         return self.job_histories[job_id]
    #     return []
