import os

class Builder(object):
    def __init__(self, name: str):
        self.name = name

    def build_img(self, tag: str):
        os.system(f"docker build -t svtter/{self.name}:{tag} .")

    def build_venv(self):
        os.system(f"docker build -f dockerfile.venv -t svtter/{self.name}-venv:latest .")
