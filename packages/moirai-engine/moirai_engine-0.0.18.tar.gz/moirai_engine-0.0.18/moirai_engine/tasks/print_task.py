import asyncio
from moirai_engine.tasks.task import Task, TaskStatus
from moirai_engine.sockets.socket import SocketType


class PrintTask(Task):
    def __init__(self, id: str, label: str = "Print Task", description: str = ""):
        super().__init__(id, label, description)
        input_1 = self.create_input("input_string", "Input", SocketType.String)
        input_1.allow_direct_input = True

    async def execute(self):
        input_string = self.get_input("input_string")
        self.notify(input_string.get_value())  # This is not working
        # print(input_string.get_value())  # This is not working
        self.status = TaskStatus.COMPLETED
