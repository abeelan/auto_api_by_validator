"""
Built-in validate comparators.
"""

import re
import logging


def _isinstance(actual, expect):
    if type(actual) is int:
        return "int"
    elif type(actual) is float:
        return "float"
    elif type(expect) is str:
        return "str"

    if isinstance(actual, type(expect)):
        return "isinstance"
    else:
        error_message = "FAIL, TypeError: actual[{}] type is {}, expect[{}] type is {}".format(
            actual, type(actual), expect, type(expect)
        )
        logging.error(error_message)
        raise TypeError(error_message)


def _exception_handling(compare_content, success_message, error_message):
    try:
        assert compare_content
        logging.info(success_message)
    except AssertionError:
        logging.error(error_message)
        raise AssertionError(error_message)


def _cast_to_int(arg):
    try:
        return int(arg)
    except Exception:
        raise AssertionError("%r can't cast to int" % str(arg))


def equals(actual, expect):
    date_type = _isinstance(actual, expect)
    if date_type == "str" and expect.lower() in ["true", "false"]:
        is_boolean(actual, expect)
    else:
        if date_type == "int":
            actual = _cast_to_int(actual)
            expect = _cast_to_int(expect)
        elif date_type == "float":
            actual = float(actual)
            expect = float(expect)
        elif date_type == "isinstance":
            expect = expect
        _exception_handling(
            actual == expect,
            "PASS, AssertValueEquals, actual[{}] == expect[{}]".format(actual, expect),
            "FAIL, ValueNotEqualsError, actual[{}], expect[{}]".format(actual, expect)
        )


def num_equals(actual, expect):
    """
    断言数字类型 强制转为 int
    equals() 已经兼容该方法
    """
    actual = _cast_to_int(actual)
    expect = _cast_to_int(expect)

    _exception_handling(
        actual == expect,
        "PASS, AssertNumberEquals, actual[{}] == expect[{}]".format(actual, expect),
        "FAIL, NumberNotEqualsError, actual[{}], expect[{}]".format(actual, expect)
    )


def not_equals(actual, expect):
    if _isinstance(actual, expect) == "int":
        actual = _cast_to_int(actual)
        expect = _cast_to_int(expect)
    elif _isinstance(actual, expect) == "float":
        actual = float(actual)
        expect = float(expect)
    elif _isinstance(actual, expect) == "isinstance":
        actual = actual
        expect = expect
    _exception_handling(
        actual != expect,
        "PASS, AssertValueNotEquals, actual[{}] != expect[{}]".format(actual, expect),
        "FAIL, ValueEqualsError, actual[{}], expect[{}]".format(actual, expect)
    )


def less_than(actual, expect):
    actual = type(expect)(actual)
    if _isinstance(actual, expect):
        _exception_handling(
            actual < expect,
            "PASS, actual[{}] < expect[{}]".format(actual, expect),
            "FAIL, actual[{}] not less than expect[{}]".format(actual, expect)
        )


def less_than_or_equals(actual, expect):
    actual = type(expect)(actual)
    if _isinstance(actual, expect):
        _exception_handling(
            actual <= expect,
            "PASS, actual[{}] < expect[{}]".format(actual, expect),
            "FAIL, actual[{}] not less than or equals expect[{}]".format(actual, expect)
        )


def greater_than(actual, expect):
    actual = type(expect)(actual)
    if _isinstance(actual, expect):
        _exception_handling(
            actual > expect,
            "PASS, actual[{}] > expect[{}]".format(actual, expect),
            "FAIL, actual[{}] not greater than expect[{}]".format(actual, expect)
        )


def greater_than_or_equals(actual, expect):
    actual = type(expect)(actual)
    if _isinstance(actual, expect):
        _exception_handling(
            actual >= expect,
            "PASS, actual[{}] >= expect[{}]".format(actual, expect),
            "FAIL, actual[{}] not greater than or equals expect[{}]".format(actual, expect)
        )


def length_equals(actual, expect):
    if not isinstance(expect, int):
        expect = _cast_to_int(expect)

    _exception_handling(
        len(actual) == expect,
        "PASS, actual[{}] length is {}, with the expect[{}] equals.".format(actual, len(actual), expect),
        "FAIL, actual[{}] length is {}, with the expect[{}] not equals.".format(actual, len(actual), expect)
    )


def length_greater_than(actual, expect):
    if not isinstance(expect, int):
        expect = _cast_to_int(expect)

    _exception_handling(
        len(actual) > expect,
        "PASS, actual[{}] length is {}, greater than expect[{}].".format(actual, len(actual), expect),
        "FAIL, actual[{}] length is {}, not greater than expect[{}].".format(actual, len(actual), expect)
    )


def length_greater_than_or_equals(actual, expect):
    if not isinstance(expect, int):
        expect = _cast_to_int(expect)

    _exception_handling(
        len(actual) >= expect,
        "PASS, actual[{}] length is {}, greater than or equals expect[{}].".format(actual, len(actual), expect),
        "FAIL, actual[{}] length is {}, not greater than or equals expect[{}].".format(actual, len(actual), expect)
    )


def length_less_than(actual, expect):
    if not isinstance(expect, int):
        expect = _cast_to_int(expect)

    _exception_handling(
        len(actual) < expect,
        "PASS, actual[{}] length is {}, less than expect[{}].".format(actual, len(actual), expect),
        "FAIL, actual[{}] length is {}, not less than expect[{}].".format(actual, len(actual), expect)
    )


def length_less_than_or_equals(actual, expect):
    if not isinstance(expect, int):
        expect = _cast_to_int(expect)

    _exception_handling(
        len(actual) < expect,
        "PASS, actual[{}] length is {}, less than or equals expect[{}].".format(actual, len(actual), expect),
        "FAIL, actual[{}] length is {}, not less than or equals expect[{}].".format(actual, len(actual), expect)
    )


def expect_in_actual(actual, expect):
    assert isinstance(actual, (list, tuple, dict, str, bytes))
    _exception_handling(
        expect in actual,
        "PASS, AssertExpectInActual, expect[{}] in actual[{}]".format(expect, actual),
        "FAIL, AssertExpectNotInActual, expect[{}] not in actual[{}]".format(expect, actual)
    )


def actual_in_expect(actual, expect):
    assert isinstance(expect, (list, tuple, dict, str, bytes))
    _exception_handling(
        actual in expect,
        "PASS, AssertActualInExpect, actual[{}] in expect[{}]".format(actual, expect),
        "FAIL, AssertActualNotInExpect, actual[{}] not in expect[{}]".format(actual, expect)
    )


def regex_match(actual, expect):
    r""" 从字符串起始位置去匹配正则表达式

    re.match(pattern, string, flags=0)

    Example:
        content = 'Hello 123456789 Word_This is just a test'
        result = re.match('^Hello\s\d{9}.*test$', content)
        # ^ 标识开头，这里匹配以Hello开头的字符串
        # $ 标识结尾，这里匹配以test结尾的字符串
        # \s 匹配空白字符串
        # \d{9} 匹配9位数字
        # . 匹配除了换行符之外的任意字符，*匹配零次或多次，二者结合起来能够匹配任意字符（除换行符）
        print(result)
        print(result.group()）  # group() 输出匹配到的内容
        print(result.span())   # span() 输出匹配的范围

        <_sre.SRE_Match object; span=(0, 40), match='Hello 123456789 Word_This is just a test'>
        Hello 123456789 Word_This is just a test
        (0, 40)
    """
    assert isinstance(actual, str)
    assert isinstance(expect, str)
    _exception_handling(
        re.match(expect, actual),
        "PASS, RegexMatch, actual[{}], pattern [{}]".format(actual, expect),
        "FAIL, RegexMatchError, actual[{}], pattern [{}]".format(actual, expect)
    )


def startswith(actual, expect):
    if isinstance(actual, str) and isinstance(expect, str):
        _exception_handling(
            actual.startswith(expect),
            "PASS, AssertActualStartswithExcept, actual[{}] startswith expect[{}]".format(actual, expect),
            "FAIL, AssertActualNotStartswithExcept, actual[{}] not startswith expect[{}]".format(actual, expect)
        )


def endswith(actual, expect):
    if isinstance(actual, str) and isinstance(expect, str):
        _exception_handling(
            actual.endswith(expect),
            "PASS, AssertActualEndswithExcept, actual[{}] endswith expect[{}]".format(actual, expect),
            "FAIL, AssertActualNotEndswithExcept, actual[{}] not endswith expect[{}]".format(actual, expect)
        )


def is_switch(actual, expect=""):
    actual = _cast_to_int(actual)
    if expect == "":
        actual_in_expect(actual, [0, 1])
    else:
        actual_in_expect(actual, expect)


def is_boolean(actual, expect):
    exp = str(expect).lower()
    act = str(actual).lower()
    if exp == "true":
        _exception_handling(
            act == exp,
            "PASS, actual[{}] is True.".format(actual),
            "FAIL, except is [{}], but actual is [{}].".format(expect, actual)
        )
    elif exp == "false":
        _exception_handling(
            act == exp,
            "PASS, actual[{}] is False.".format(actual),
            "FAIL, except is [{}], but actual is [{}].".format(expect, actual)
        )
    else:
        _exception_handling(
            act in ["true", "false"],
            "PASS, actual[{}] is a boolean!".format(actual),
            "FAIL, actual[{}], It's not a boolean!".format(actual)
        )


def is_none(actual):
    _exception_handling(
        actual is None,
        "PASS, actual[{}] is None.".format(actual),
        "FAIL, actual[{}] not is None.".format(actual)
    )


def is_not_none(actual):
    _exception_handling(
        actual is not None,
        "PASS, actual[{}] is not None.".format(actual),
        "FAIL, actual[{}] is None.".format(actual)
    )


def str_repeat_count_equals(string: str, expect: tuple):
    """
    统计目标字符在字符串内出现的次数 相等

    :param string: str 实际返回结果
    :param expect: tuple (str，int)
    :return: boolean

    Example:
        str_repeat_count_equals("123|123|123|123", ("|", "3"))
    """
    target = expect[0]
    exp_count = expect[1]
    if isinstance(exp_count, str):
        exp_count = _cast_to_int(exp_count)

    str_count_dict = dict()
    for i in string:
        str_count_dict[i] = str_count_dict.get(i, 0) + 1
    act_count = str_count_dict[target]

    _exception_handling(
        exp_count == act_count,
        f"PASS, StrRepeatCountEquals, [\"{target}\"] repeat count ：actual[{act_count}], expect[{exp_count}]",
        f"FAIL, StrRepeatCountNotEquals, [\"{target}\"] repeat count ：actual[{act_count}], expect[{exp_count}]"
    )


class AssertMethods:
    """ 封装了下字符串以供调用

    :return str

    # 字符串在该函数内进行处理
    validate.py
        _run_validator()
    """
    @staticmethod
    def equals():
        return "equals"

    @staticmethod
    def not_equals():
        return "not_equals"

    @staticmethod
    def less_than():
        return "less_than"

    @staticmethod
    def less_than_or_equals():
        return "less_than_or_equals"

    @staticmethod
    def greater_than():
        return "greater_than"

    @staticmethod
    def greater_than_or_equals():
        return "greater_than_or_equals"

    @staticmethod
    def length_equals():
        return "length_equals"

    @staticmethod
    def length_greater_than():
        return "length_greater_than"

    @staticmethod
    def length_greater_than_or_equals():
        return "length_greater_than_or_equals"

    @staticmethod
    def length_less_than():
        return "length_less_than"

    @staticmethod
    def length_less_than_or_equals():
        return "length_less_than_or_equals"

    @staticmethod
    def expect_in_actual():
        return "expect_in_actual"

    @staticmethod
    def actual_in_expect():
        return "actual_in_expect"

    @staticmethod
    def regex_match():
        return "regex_match"

    @staticmethod
    def startswith():
        return "startswith"

    @staticmethod
    def endswith():
        return "endswith"

    @staticmethod
    def is_switch():
        return "is_switch"

    @staticmethod
    def is_boolean():
        return "is_boolean"

    @staticmethod
    def is_none():
        return "is_none"

    @staticmethod
    def is_not_none():
        return "is_not_none"

    @staticmethod
    def str_repeat_count_equals():
        return "str_repeat_count_equals"


if __name__ == '__main__':
    # str_repeat_count_equals("123|123|123|123", ("|", "3"))
    pass