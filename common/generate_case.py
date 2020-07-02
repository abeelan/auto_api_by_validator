import os
from common import utils
from common import path
from common import convert
from config import parser_yaml


def generate_case(feature, api_name):
    case = f"""
import pytest
import allure
from common import request
from common import validate
from common.comparators import AssertMethods as am


file_path = __file__


@allure.feature("{feature}")
class Test{convert.convert_str_to_hump(api_name.split(".")[0])}:

    @allure.story("{api_name}")
    @allure.title("-- 用例名称 --")
    @allure.severity(allure.severity_level.NORMAL)
    def test_case_01(self, get_api, common_params):
    
        with allure.step("第一步：发送请求，获取响应实体"):
            response = request.get(url=get_api, params=common_params)
            result = response.json()
            
            allure.attach(response.url, "请求", allure.attachment_type.TEXT)
            allure.attach(response.text, "响应", allure.attachment_type.TEXT)

        with allure.step("第二步：运行断言器"):
            if validate.assert_code(response.status_code, 200):
                # 1. 首次生成 case，需要运行一次获取到 response，生成 validator
                validate.gen_validator(file_path, result)
                
                # 2. 生成 validator 成功后，取消掉注释，即可正常运行断言器
                # validate.run_validator(validator, result)
                
    def test_case_02(self):
        pytest.skip("此为测试启动方法, 不执行")
                

if __name__ == '__main__':

    pytest.main([__file__])

"""

    # 创建模块目录
    feature_path = os.path.join(path.case_path(), feature)
    utils.mkdir(feature_path)

    # 创建用例文件
    test_path = os.path.join(feature_path, "test_{}.py".format(api_name.split(".")[0]))
    utils.create_file(test_path, case)


def gen_all_case():
    """ 生成 config/all_api.yml 内所有 case
    """
    all_api = parser_yaml.load_yaml(os.path.join(path.config_path(), "all_api.yml"))
    for k, v in all_api.items():
        if v:  # 判断 feature 不为空
            api_items = str(v).split(" ")
            for api in api_items:
                generate_case(k, api)


if __name__ == '__main__':
    _api_name = "chargeChapter.m"
    _feature = "basicInfo"
    generate_case(_feature, _api_name)

    # gen_all_case()

