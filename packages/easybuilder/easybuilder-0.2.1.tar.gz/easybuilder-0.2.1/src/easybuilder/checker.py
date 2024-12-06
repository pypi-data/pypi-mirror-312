import os

from loguru import logger


def check_clean(folder: str = "."):
    # 检查git仓库是否有未提交的更改
    os.chdir(folder)
    result = os.popen("git status --porcelain").read()
    if not os.path.exists(".git"):
        logger.error("错误: 当前目录不是git仓库")
        exit(1)
    if result:
        logger.error("错误: git仓库不干净,请先提交所有更改")
        logger.error("未提交的更改:")
        logger.error(result)
        exit(1)
    logger.info("git仓库状态检查通过")
