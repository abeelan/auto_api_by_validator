
import pytest
import allure
from common import request
from common import validate
from common.comparators import AssertMethods as am


file_path = __file__

validator = {
  "errorlog": {
    "actual": "",
    "compare": am.regex_match(),
    "expect": "版本.*。$"
  },
  "success": {
    "actual": "",
    "compare": am.is_boolean(),
    "expect": "false"
  }
}


@allure.feature("appControl")
@allure.story("验证版本更新")
class TestCheckVersion:

    @allure.title("验证版本无更新情况")
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
                validate.run_validator(validator, result)
                
    def test_case_02(self):
        pytest.skip("此为测试启动方法, 不执行")
                

if __name__ == '__main__':
    pytest.main()


