"""
生成校验器 并运行
"""
import re
import json
import logging

from common import utils
from common import convert
from common import comparators
from common.comparators import AssertMethods as am


def gen_validator(case_path, response):
    """ 读取case文件内是否存在断言器，如果没有则创建

    Example:
        >>> gen_validator(__file__, response.json())
    """
    with open(case_path, "r+") as f:
        if re.search("validator =", f.read()):
            logging.info("validator is existing...")
        else:
            logging.info("validator generated...")
            validator = convert.convert_json_to_validate_dict(response)
            content = "validator = {}".format(
                json.dumps(validator, sort_keys=True, indent=2, ensure_ascii=False)
            )
            utils.insert_content_into_keyword_next_line(case_path, content, keyword="__file__")


def run_validator(validator, response):
    """ 运行断言器 根据验证条件 比对实际与预期的值

    Args:
        validator: case 文件内的变量，由 gen_validator() 函数生成
        response : 响应实际返回内容（json）

    Example:
        >>> run_validator(validator, response.json())
    """
    # 将 response 返回值填入到 validator 内
    act_validator = convert.add_act_value_to_validate_dict(validator, response)
    logging.info("Running validator >>>")
    _run_validator(act_validator)
    logging.info("Run finished <<<")


def _run_validator(json_dict):
    """ 传入 validator 数据类型，递归断言
    """
    if isinstance(json_dict, dict):
        for k, v in json_dict.items():
            if isinstance(v, dict) and "actual" in v.keys():
                act = v["actual"]
                exp = v["expect"]
                cmp = v["compare"]
                logging.info("--> {}".format(k))

                if cmp == "equals" or cmp == "=":
                    comparators.equals(act, exp)
                elif cmp == "num_equals":
                    comparators.num_equals(act, exp)
                elif cmp == "not_equals" or cmp == "!=":
                    comparators.not_equals(act, exp)
                elif cmp == "greater_than" or cmp == ">":
                    comparators.greater_than(act, exp)
                elif cmp == "greater_than_or_equals" or cmp == ">=" or cmp == "=>":
                    comparators.greater_than_or_equals(act, exp)
                elif cmp == "less_than" or cmp == "<":
                    comparators.less_than(act, exp)
                elif cmp == "less_than_or_equals" or cmp == "<=" or cmp == "=<":
                    comparators.less_than_or_equals(act, exp)

                elif cmp == "length_equals":
                    comparators.length_equals(act, exp)
                elif cmp == "length_greater_than":
                    comparators.length_greater_than(act, exp)
                elif cmp == "length_greater_than_or_equals":
                    comparators.length_greater_than_or_equals(act, exp)
                elif cmp == "length_less_than":
                    comparators.length_less_than(act, exp)
                elif cmp == "length_less_than_or_equals":
                    comparators.length_less_than_or_equals(act, exp)

                elif cmp == "str_repeat_count_equals":
                    comparators.str_repeat_count_equals(act, exp)

                elif cmp == "actual_in_expect":
                    comparators.actual_in_expect(act, exp)
                elif cmp == "expect_in_actual":
                    comparators.expect_in_actual(act, exp)

                elif cmp == "startswith":
                    comparators.startswith(act, exp)
                elif cmp == "endswith":
                    comparators.endswith(act, exp)

                elif cmp == "regex_match":
                    comparators.regex_match(act, exp)

                elif cmp == "is_switch":
                    comparators.is_switch(act, exp)
                elif cmp == "is_none":
                    comparators.is_none(act)
                elif cmp == "is_not_none":
                    comparators.is_not_none(act)
                elif cmp == "is_boolean" or "is_bool":
                    comparators.is_boolean(act, exp)

                else:
                    error_message = "Please check 'compare' value! Not found '{}' in validate!".format(cmp)
                    logging.error(error_message)
                    raise AssertionError(error_message)

            elif isinstance(v, list):
                # 当断言器内存在列表时，循环读取列表内数据，再次递归断言
                for data in v:
                    _run_validator(data)

            else:
                _run_validator(v)


def assert_code(code, expected_code):
    try:
        assert code == expected_code
        logging.info("AssertCode, actual[{}] == expect[{}]".format(
                code, expected_code)
        )
        return True
    except AssertionError:
        error_message = "StatusCodeError, status code[{}], expect code[{}]".format(code, expected_code)
        logging.error(error_message)
        raise AssertionError(error_message)


if __name__ == '__main__':
    # assert_code(200, 200)
    # assert_code(200, 300)
    # assert_equal('a', 'a')
    # assert_equal('a', 'b')
    # assert_in('a', 'ab')
    # assert_in('a', 'bc')
    # assert_in('a', ['c'])
    # assert_is_switch(1)
    # assert_is_switch(3)
    __r = {
        "promotionItems":[
            {
                "name": "name 1",
                "id": "id 1"
            },
            {
                "name": "name 2",
                "id": "id 2"
            }
    ]
    }
    __a = {
        'promotionItems': [
            {
                'name': {'actual': '', 'compare': 'equals', 'expect': 'name 1'},
                'id': {'actual': '', 'compare': 'equals', 'expect': 'id 1'},
            },
            {
                'name': {'actual': '', 'compare': 'equals', 'expect': 'name 2'},
                'id': {'actual': '', 'compare': 'equals', 'expect': 'id 2'},

            },
    ]
    }

    value_list = {
        "name": {'actual': '', 'compare': 'is_none', 'expect': 'name 1'},
        'id': {'actual': '', 'compare': 'equals', 'expect': 'id 1'}
    }

    resp = {
        'name': 'name 1',
        'id': 'id 1'
    }
    # act_validator = convert.add_act_value_to_validate_dict(__a, __r)
    # act_validator = convert.add_act_value_to_validate_dict(value_list, resp)
    # _run_validator(act_validator)
    pass
