"""
获取配置文件内的数据
"""
import os
import logging

from common import path
from config.parser_conf import Config
from config.parser_yaml import load_yaml


class GetParamsIni:

    def __init__(self):
        self.config = Config(os.path.join(path.config_path(), "params.ini"))

    def get_timeout(self):
        return self.config.get_value("default", "timeout")

    def get_params(self):
        return {k: v for k, v in self.config.get_section_items("params")}

    def get_spec_params(self):
        return {k: v for k, v in self.config.get_section_items("spec_params")}

    @staticmethod
    def get_host(_os="android", _app="easou", _env="test"):
        """获取 api 和 webview 的域名
        """
        if _os in ["android", "ios"] and _app in ["easou", "kuaidu"] and _env in ["test", "online"]:
            path = '{}/env.yml'.format(os.path.dirname(__file__))
            content = load_yaml(path)

            address = "api/bookapp/"
            api = content[_os][_app][_env]["api"]
            webview = content[_os][_app][_env]["web"]

            if api and webview:
                return api+address, webview
            else:
                logging.error("api: {}, webview: {}".format(api, webview))
                logging.error("api or webview is None, please check env.yml")
        else:
            log = """请输入正确的参数：
_os    :  android | ios
_app   :  easou   | other
_env   :  test    | online
"""
            logging.error(log)

    def get_account(self):
        account_items = self.config.get_section_items("account")
        account_dict = {}
        for item in account_items:
            account_dict[item[0]] = item[1]
        return account_dict

    def user_info(self, key):
        return self.get_account()[key]


if __name__ == '__main__':
    # GetParamsIni().get_host(_env="ss")
    print(GetParamsIni().user_info("username"))