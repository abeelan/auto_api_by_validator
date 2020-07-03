import os
import nose
import pytest
import allure
import logging

from config import get_params_ini
from config import parser_yaml
from config import parser_conf

from common import logger
from common import path
logger.Logging()

"""
# @allure.feature  # 用于定义被测试的功能模块
# @allure.story    # 用于定义被测功能的用户场景
# @allure.title    # 用于定义用例名称
# @allure.severity # 用于定义用例优先级
# @allure.issue    # 用于定义问题表识，关联标识已有的问题，可为一个url链接地址
# @allure.testcase # 用于用例标识，关联标识用例，可为一个url链接地址
# @allure.attach   # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
# @allure.step     # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
"""


def pytest_collection_modifyitems(items):
    """ 测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
        修改编码格式，解决用例名称包含中文乱码的问题
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


def pytest_addoption(parser):
    """ 设置命令行参数
    """
    parser.addoption(
        "--os", action="store", default="android", help="os : android or ios"
    )
    parser.addoption(
        "--app", action="store", default="easou", help="app : easou or kuaidu"
    )
    parser.addoption(
        "--env", action="store", default="online", help="env : test or online"
    )


@pytest.fixture(scope="session")
def get_option(request):
    _os = request.config.getoption("--os")
    _app = request.config.getoption("--app")
    _env = request.config.getoption("--env")
    return _os, _app, _env


@pytest.fixture(scope="session")
def get_host(get_option):
    """ 根据命令行传参获取对应的 api 和 webview
    """
    host = get_params_ini.GetParamsIni().get_host(
        _os=get_option[0],
        _app=get_option[1],
        _env=get_option[2],
    )
    api = host[0]
    webview = host[1]
    return api, webview


@pytest.fixture(scope="module")
def get_api(request, get_host):
    """ 将 host 与 api 进行拼接
    """
    file_path = getattr(request.module, "file_path")
    file_name = os.path.split(file_path)[-1].replace("py", "m")
    api = file_name.split("_", 1)[1]
    return get_host[0] + api


@pytest.fixture(scope="session")
def get_webview(get_host):
    return get_host[1]


@pytest.fixture(scope="module")
def common_params():
    """ 获取公共参数
    """
    return get_params_ini.GetParamsIni().get_params()


@pytest.fixture()
def get_ini():
    return get_params_ini.GetParamsIni()


# def pytest_sessionfinish(session):
#     """ set allure report environment
#     """
#     project_path = os.path.dirname(session.config.rootdir)
#     env_cfg_path = "".join([os.path.dirname(project_path), "/report/environment.properties"])
#
#     with open(env_cfg_path, "w") as f:
#         # host = get_host()
#         # env = "API=%s\nWEBVIEW=%s\n" % (host[0], host[1])
#         # TODO: 如何将获取到的api、webview，传入进来。。。用上面那行不生效。。。
#         env = """
# API={}
# WEBVIEW={}
# """.format(..., ...)
        # f.write(env)




