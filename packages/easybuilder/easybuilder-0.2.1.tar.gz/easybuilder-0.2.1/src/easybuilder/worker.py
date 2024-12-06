import loguru

from . import task


class Worker(object):
    default_tasks: list[type[task.Task]] = [task.CheckCleanTask]
    prev_tasks: list[type[task.Task]] = []
    next_tasks: list[type[task.Task]] = []

    def __init__(self):
        pass

    def get_logger(self):
        """using loguru for logger"""
        return loguru.logger

    def before_run(self):
        for t in self.default_tasks:
            t().action()
        for t in self.prev_tasks:
            t().action()

    def after_run(self):
        pass

    def main(self):
        """user implement this"""
        pass

    def run(self):
        self.before_run()
        self.main()
        self.after_run()
