import os
import time

import pytest

from easybuilder.checker import check_clean
from easybuilder.temputils import TempFolder


@pytest.fixture
def create_dirty_temp_repo():
    with TempFolder() as tmp_folder:
        os.chdir(tmp_folder)
        os.system("git init")
        with open("README.md", "w") as f:
            f.write("test")

        # not clean
        yield tmp_folder


@pytest.fixture
def create_clean_temp_repo():
    with TempFolder() as tmp_folder:
        os.chdir(tmp_folder)
        os.system("git init")
        yield tmp_folder


def test_no_git(create_dirty_temp_repo):
    # we should create a new directory and check it
    with pytest.raises(SystemExit):
        check_clean(create_dirty_temp_repo)


def test_clean(create_clean_temp_repo):
    check_clean(create_clean_temp_repo)
