# README
接口自动化测试实现：
> pytest + request + allure

V1.0 版本 [初探 API 自动化测试](https://mp.weixin.qq.com/s?__biz=MzU2NzM4MTUxNw==&mid=2247483788&idx=1&sn=dc54a57afaeffeb2cd37a1c39e38ced1&chksm=fc9f5aeecbe8d3f8226624cb26dd07759d629597ce474a3a7e990b54396e1218989f0c100260&scene=21#wechat_redirect)

写出来的自动化脚本存在一些问题，针对遇到的问题进行了部分优化，问题记录可查看该文章：

[关于接口自动化测试的思考与改进](https://mp.weixin.qq.com/s/SldOQI9XeDu9-Lw1Qb0ASA)

项目预览
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200703163640432.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xhbl95YW5nYmk=,size_16,color_FFFFFF,t_70)
**修改记录**
@[toc]
# pytest 替代 unittest
## conftest.py
用例内必要的参数可以封装到 `conftest.py` 内，方便调用，比如：
- host
- 公共参数
- 特殊参数
- 获取配置信息
- ...

以公共参数为例：
```python
# conftest.py
@pytest.fixture(scope="module")
def common_params():
    """ 获取公共参数
    """
    return get_params_ini.GetParamsIni().get_params()
```
那么在用例内就可以直接使用，省去了之前每条 case 模块 `setup` 获取公共参数及 host 的冗余。
```python
# testcase.py
import pytest
def test_case_02(self, common_params):
	print(common_params)
    pytest.skip("此为测试启动方法")
```
## 参数化
pytest 还有一大亮点是参数化，这样只用设计用例数据就可以啦。
```python
@pytest.mark.parametrize(
        "num, result",
        [(-1, "fail"), (5, "pass"), (0, "error")]
    )
def test_case_01(self, num, result):
	if num > 0:
		assert result == "pass"
	elif num < 0:
		assert result == "fail"
	else:
		assert result == "error"
```
## 指定用例
```python
 pytest.main(["-q", "-s", 用例模块1, 用例模块2])
```

# 日志记录
重新封装 `logging` 模块，记录每次运行用例的详细信息
```python
class Logging:
    """setup logging

    Examples:
        >>> import logging
        >>> Logging()
        >>> logging.debug("this is debug message")

        /log/2020-04-30.log

        [DEBUG - 2020-04-30 15:26:40,033 - logger.py] : this is debug message
    """
```

# 断言器
```python
def test_case_01(self, get_api, common_params):
        response = request.get(url=get_api, params=common_params)
        result = response.json()

        if response.raise_for_status():
            # 1. 首次生成 case，需要运行一次获取到 response，生成 validator
            validate.gen_validator(file_path, result)
                
            # 2. 生成 validator 成功后，取消掉注释，即可正常运行断言器
            # validate.run_validator(validator, result)
```
上面就是写出来的case，运行步骤如下：
1. 请求接口，获取到响应实体（JSON）；
2. 判断状态码为 200，证明接口请求成功；
3. 根据响内容生成断言器（validator），填充在该 py 文件头部；
4. 修改断言器的内容，取消代码中的第2步 ` # validate.run_validator(validator, result)`注释；
5. 再次运行，即可按照断言器的预期是做比较。

**什么是断言器？**

拿请求版本更新的接口返回值为例：

```json
{
	"success": true,
	"errorlog": "版本无更新。"
}
```

一般我们这样断言：

```python
assert result["succese"] == True
assert result["errorlog"] == "版本无更新。"
```

但是当接口字段非常多的时候，会写非常多的assert来校验，接口字段变动，也会很难维护。所以根据响应值生成一个断言器，断言器就是将```RESPONSE```转为一个容易维护的数据格式：

```json
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
```
将每个字段的值拆分为 
- 实际值(actual)
- 断言方式(compare)
- 预期值(expect)

断言器生成后会将请求的响应值自动填入预期内，作为判断的标准。
部分字段需要修改，可以在 `validator` 中修改 compare 和 expect 。

上面例子的断言内容为：
1. errorlog 字段使用正则表达式判断是否以“版本”两个字开始，以句号结尾。可以模糊断言“版本有更新。”和“版本无更新。”的情况。
2. success 字段为布尔值，通过 `is_boolean()` 方法判断返回值的类型，再与预期做比较。

判断的方法还有很多，基本都做了封装。

# allure
>Allure框架是一种灵活的轻量级多语言测试报告工具，它不仅能够以简洁的web报告形式显示已测试的内容，而且允许参与开发过程的每个人从测试的日常执行中提取最大限度的有用信息。

pytest 支持 allure 生成报告，使用方便。

使用方法：
```python
@allure.feature  # 用于定义被测试的功能模块
@allure.story    # 用于定义被测功能的用户场景
@allure.title    # 用于定义用例名称
@allure.severity # 用于定义用例优先级
@allure.issue    # 用于定义问题表识，关联标识已有的问题，可为一个url链接地址
@allure.testcase # 用于用例标识，关联标识用例，可为一个url链接地址
@allure.attach   # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
@allure.step     # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
```

所以最后的用例是这样子的：
```python
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

				validator["errorlog"]["expect"] = "版本无更新。"  # 修改断言器内的值
                
                # 2. 生成 validator 成功后，取消掉注释，即可正常运行断言器
                validate.run_validator(validator, result)
                
    def test_case_02(self):
        pytest.skip("验证版本有更新。")
                

if __name__ == '__main__':
    pytest.main()
```

生成的allure报告展示如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200703160258301.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xhbl95YW5nYmk=,size_16,color_FFFFFF,t_70)
# 自动生成用例模版
写用例过程中发现其实上面完成的那条用例，大部分代码是可以复用在其他用例上的。
如：alllure 装饰器的调用，接口请求值的获取，每条用例都是一样的。

因为有固定的模版，所有就可以根据接口名称来生成测试用例。

```python
def generate_case(feature, api_name):
	""" 模块、接口名称
	Example:
		>>> generate_case("appControl", "checkVersion")

		1. 在case目录下，创建 appControl 文件夹，
		2. 文件夹内创建 test_checkVersion.py 文件
		3. 文件内写入模版 case
	"""
	pass
```
通过这种方式，还可以实现批量新建case模版，将所有的接口按模块写入到yml文件内，遍历该 yml 文件，生成全部case，然后再逐条调试。
```yml
# all_api.yml
appControl:
  check_version.m
  test_api.m

feature:
  feature_test_api.m
```
生成后效果如下：
```bash
case/
	appControl/
		test_check_version.py
		test_test_api.py
	feature/
		test_feature_test_api.py
```
