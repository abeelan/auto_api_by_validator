import os
import sys
import time
import logging

from common.utils import mkdir


class Logging:
    """setup logging

    Examples:
        >>> import logging
        >>> Logging()
        >>> logging.debug("this is debug message")

        /log/2020-04-30.log

            [DEBUG - 2020-04-30 15:26:40,033 - logger.py] : this is debug message
    """

    def __init__(self):
        """ settings logging
        """
        """
            第一步，初始化 log 目录
        """
        day_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 2020-04-20
        minutes_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 2020-04-20

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目路径

        log_folder = "{}/log".format(path)
        log_child_folder = "{}/log/{}".format(path, day_time)

        mkdir(log_folder)
        # mkdir(log_child_folder)

        # log - 2020-04-30 - 2020-04-30-14-20.log
        # log_file = "{}/{}.log".format(log_child_folder, minutes_time)
        # log_err_file = "{}/{}_error.log".format(log_child_folder, minutes_time)

        # log - 2020-04-30.log 因为按分钟写入log文件太频繁，改成按天写入log 并取消二级目录
        log_file = "{}/{}.log".format(log_folder, day_time)

        """
            第二步，创建一个handler，用于写入全部info日志文件
        """
        # a 代表继续写log，不覆盖之前log
        # w 代表重新写入，覆盖之前log
        file_handler = logging.FileHandler(log_file, mode='a+')
        file_handler.setLevel(logging.DEBUG)

        """
            第三步，创建一个handler，用于写入错误日志文件
        """
        # 由于 error log 文件只写入错误行内容，已经在log文件内覆盖，所以没必要
        # error_file_handler = logging.FileHandler(log_err_file, mode='a+')
        # error_file_handler.setLevel(logging.ERROR)

        """
            第四步，再创建一个handler，用于输出到控制台
        """
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)

        """
            第五步，定义handler的输出格式
        """
        formatter = logging.Formatter(
            "[%(levelname)s - %(asctime)s - %(filename)s] : %(message)s"
        )
        file_handler.setFormatter(formatter)
        # error_file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)

        """
            第六步，将logger添加到handler里面
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.handlers = []

        logger.addHandler(file_handler)
        # logger.addHandler(error_file_handler)
        logger.addHandler(stdout_handler)


if __name__ == '__main__':
    Logging()
    logging.debug("test")
    logging.error("test")
