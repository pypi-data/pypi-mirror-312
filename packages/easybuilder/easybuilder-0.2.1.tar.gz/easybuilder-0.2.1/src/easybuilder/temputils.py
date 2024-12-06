import shutil
import tempfile


class TempFolder:
    def __init__(self):
        self.folder = tempfile.mkdtemp()

    def __enter__(self):
        return self.folder

    def __exit__(self, exc_type, exc_value, traceback):
        # shutil.rmtree(self.folder)
        pass
