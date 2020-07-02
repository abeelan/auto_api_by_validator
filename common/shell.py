import os
import subprocess
import time


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()
        o = output.decode("utf-8")
        return o


class System:

    def __init__(self):
        pass

    @classmethod
    def shell(cls, cmd, log=True):
        """
        实现命令执行，并输出log
        :param cmd: 所需要运行的系统命令
        :param log: True输出过程log，False不输出
        :return: code, log[]
        """
        logs = []
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while p.poll() is None:
            __log = p.stdout.readline()
            if log:
                print("[SHELL]%s" % __log)
            logs.append(__log)
            time.sleep(0.1)
        for __log in p.stdout.readlines():
            if log:
                print("[SHELL]%s" % __log)
            logs.append(__log)
        return p.wait(), logs

    @classmethod
    def shell_simple(cls, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logs = p.stdout.readlines()
        return p.wait(), logs

    @classmethod
    def set_env(cls, var_name, value, rewrite=False):
        if os.getenv('PATH').count(':\\'):
            split = ";"
        else:
            split = ':'
        if not rewrite:
            os.environ[var_name] = os.getenv(var_name) + split + value
        else:
            os.environ[var_name] = value
        return os.getenv(var_name)