import pytest
import os
from common import logger
from common import path
from common import shell


"""
pytest 参数：

pytest -v 说明：可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等.
pytest -s 说明：输入我们用例中的调式信息，比如print的打印信息等.
pytest -m 说明：标记，执行特定的测试用例.
pytest -k 说明："关键字"执行用例包含“关键字”的用例
pytest -q 说明：简化控制台的输出，可以看出输出信息和上面的结果都不一样， 下图中有两个..点代替了pass结果
"""

"""
allure 运行参数

按 features 运行测试用例
pytest --alluredir=report/xml --allure_features=测试登陆功能 test_case.py

按 story 运行测试用例
pytest --alluredir=report/xml --allure_stories=测试登陆成功的场景 test_case.py

按 severity 运行测试用例
pytest --alluredir=report/xml --allure_severities=blocker test_case.py
"""

report_path = path.report_path()
case_path = path.case_path()


if __name__ == '__main__':
    logger.Logging()
    pytest.main(
        [
            # "-q",
            # "-s",
            case_path,
            "--os=android",
            "--app=easou",
            "--env=test",
            f"--alluredir={report_path}",
        ]
    )
    shell.Shell().invoke("allure serve %s" % path.report_path())
