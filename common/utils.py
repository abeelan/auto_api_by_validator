import os
import re
import json
import codecs
import logging
import datetime


file = __file__


def get_current_time(t=0):
    """
    四种输出格式：t=0 默认输出格式：2016-07-19 18:54:18.282000
    t=3 返回当前日期：2018-04-01
    :param t: 入参
    :return: 按格式返回当前系统时间戳
    """

    curr_time = datetime.datetime.now()
    if t == 0:
        return curr_time  # 格式：2016-07-19 18:54:18.282000
    elif t == 1:
        return curr_time.strftime('%Y-%m-%d %H:%M:%S')  # 格式：2016-07-19 18:11:04
    elif t == 2:
        return curr_time.strftime('%Y%m%d-%H%M%S')  # 格式：2016-07-19-18-11-04
    elif t == 3:
        return curr_time.strftime('%Y-%m-%d')  # 格式：2016-07-19
    else:
        print("[warning]: no format matches...pls check!")


def mkdir(dir_path):
    """ 创建路径
    """
    # 去除首位空格
    _dir = dir_path.strip()
    _dir = dir_path.rstrip("\\")
    _dir = dir_path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(_dir)

    if not is_exists:
        try:
            os.makedirs(_dir)
        except Exception as e:
            logging.error("Directory creation failed：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logging.debug("Directory already exists：%s" % str(_dir))


def insert_content_into_keyword_next_line(file_path, insert_content, keyword=""):
    """ 从匹配关键字的下一行开始，插入内容

    Arg:
        file_path: 文件绝对路径
        insert_content: 插入的内容
        keyword: 关键字

    Example:
        test.txt
            123
            keyword
            test

        insert_content_into_keyword_next_line(
            test.txt,
            "这是插入的内容",
            "keyword"
        )

    Returns:
        test.txt
            123
            keyword
            这是插入的内容
            test
    """
    with open(file_path, 'r+', encoding='utf-8') as f:
        count = 1
        while True:
            count += 1
            content = f.readline()
            # if count == int(line):  # 向给定行插入内容, 如果使用，需要传参 line
            if re.search(keyword, content):
                num = f.tell()
                text = f.read()
                f.seek(num)
                f.write(u"\n" + str(insert_content) + "\n" + text + "\n")
                break


def create_file(file_path, content):
    """ 当文件存在时，则不再创建和覆盖
    """
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        logging.info("{} is exists!".format(file_path))
        # print("{} is exists!".format(file_path))


def print_json(json_content):
    return json.dumps(json_content, sort_keys=True, indent=2)


if __name__ == '__main__':

    pass
