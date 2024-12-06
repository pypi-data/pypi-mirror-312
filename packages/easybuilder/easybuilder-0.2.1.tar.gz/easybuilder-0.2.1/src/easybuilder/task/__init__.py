import abc
import os

from easybuilder.checker import check_clean


class Task(abc.ABC):
    @abc.abstractmethod
    def action(self):
        pass


class PdmLockTask(Task):
    """test if pdm.lock is latest"""

    def action(self):
        ret = os.system("pdm lock --check")
        if ret != 0:
            print("pdm.lock is not up to date, please run 'pdm lock' first")
            exit(1)


class CheckCleanTask(Task):
    """check if git repo is clean"""

    def action(self):
        check_clean()
