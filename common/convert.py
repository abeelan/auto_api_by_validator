"""
数据类型、格式转换处理
"""
import json
from urllib.parse import unquote


def convert_list_to_dict(origin_list):
    """
    cover har data list to mapping
    Args:
        origin_list (list)
            [
                {"name": "v", "value": "1"},
                {"name": "w", "value": "2"},
            ]

    Returns:
        dict:
            {"v": "1", "w": "2"}
    """
    return {
        item["name"]: item.get("value")
        for item in origin_list
    }


def convert_data_form_to_dict(post_data):
    """ convert x_www_form_urlencoded data to dict

        Args:
            post_data (str): a=1&b=2

        Returns:
            dict: {"a":1, "b":2}

    """
    if isinstance(post_data, str):
        covert_dict = {}
        for k_v in post_data.split("&"):
            try:
                key, value = k_v.split("=")
            except ValueError:
                raise Exception(
                    "Invalid x_www_form_urlencoded data format: {}".format(post_data)
                )
            covert_dict[key] = unquote(value)  # 解码
        return covert_dict
    else:
        return post_data


def convert_json_to_validate_dict(json_dict):
    """
    Args:
        {
            "item": 1,
            "test": "ok",
            "dict1":
                {
                    "key1": "value1",
                }
        }

    Returns:
        {
            "item": {"actual": "", "validate": "equal", "expected": 1},
            "test": {"actual": "", "validate": "equal", "expected": "ok"},
            "dict1":
                {
                    "key1": {"actual": "", "validate": "equal", "expected": "value1"},
                }
        }
    """

    validate_dict = {}
    if isinstance(json_dict, dict):
        for k in json_dict:
            value = json_dict[k]
            if isinstance(value, dict):
                validate_dict[k] = convert_json_to_validate_dict(value)
            elif isinstance(value, list):
                if value:
                    validate_list = []
                    for v in value:
                        if isinstance(v, dict):
                            validate_list.append(convert_json_to_validate_dict(v))
                            validate_dict[k] = validate_list
                else:
                    # 列表为空情况
                    validate_dict[k] = {
                        "actual": '',
                        "compare": "equals",
                        "expect": []
                    }
            else:
                validate_dict[k] = {
                    "actual": '',
                    "compare": "equals",
                    "expect": "{}".format(json_dict[k]) if type(json_dict[k]) is bool else json_dict[k]
                }
                if json_dict[k] is None:
                    validate_dict[k]["compare"] = "is_none"
                    validate_dict[k]["expect"] = "null"

    return validate_dict


def add_act_value_to_validate_dict(validate_dict, response):
    """ 将实际响应值添加到断言字典 「actual」内
    """
    if isinstance(validate_dict, dict):
        for k in validate_dict:
            value = validate_dict[k]

            if isinstance(value, dict):
                if "actual" in value.keys():
                    value["actual"] = response[k]
                else:
                    # 当字典内嵌套字典时，需要递归处理下
                    add_act_value_to_validate_dict(value, response[k])

            # 当下一层的值为列表时
            elif isinstance(value, list):
                # TODO: 如果为列表时，断言器跟响应值不一定对应，断言器和响应都是根据顺序去匹配的，
                #  如果服务器返回的响应值顺序有变化可能有误差
                num = 0
                count = len(value)
                # 遍历列表内的值
                for value_list in value:

                    # 当前 k 对应的响应值，也是 list，遍历值
                    resp = response[k][num]

                    # 断言器每循环一次，响应值的列表索引+1
                    num += 1 if num < count else num

                    if isinstance(value_list, dict):
                        add_act_value_to_validate_dict(value_list, resp)
                    else:
                        pass

            else:
                add_act_value_to_validate_dict(value, response[k])

        return validate_dict

    else:
        raise AssertionError("Error, add actual value to validator fail!")


def convert_str_to_hump(string):
    """ 将字符串转化类名
        驼峰命名：仅大写首字母
        下划线命名：以下划线为分隔符，大写每个单词首字母

    string(str): 给定字符串

    Example:
        >>> convert_str_to_hump("check_version")
        >>> convert_str_to_hump("loginByPhone")

    Returns:
        CheckVersion
        LoginByPhone

    """
    mark = "_"
    if mark in string:
        str_list = str(string).split(mark)
        first = str_list[0].lower().capitalize()
        others = str_list[1:]
        others_capital = [word.capitalize() for word in others]  # str.capitalize():将字符串的首字母转化为大写
        others_capital[0:0] = [first]
        hump_string = ''.join(others_capital)  # 将list组合成为字符串，中间无连接符。
    else:
        hump_string = string.replace(string[0], string[0].capitalize(), 1)

    return hump_string


if __name__ == '__main__':
    result = {
        "item": 2,
        "test": "oo",
        "dict1":[
            {
                "key1": "value0",
                "key2": "value2",
                "key3": {"key3 - key1": "key32- value1"}
            }]
    }
    validate = {'item':
                    {'actual': '', 'compare': 'equal', 'expect': 1},
                'test':
                    {'actual': '', 'compare': 'equal', 'expect': 'ok'},
                'dict1':[
                    {'key1':
                         {'actual': '', 'compare': 'equal', 'expect': 'value1'},
                     'key2': {'actual': '', 'compare': 'equal', 'expect': 'value2'},
                     'key3': {'key3 - key1':
                                  {'actual': '', 'compare': 'equal', 'expect': 'key3 - value1'}
                              }
                     }]
                }
    # print(json.dumps(convert_json_to_validate_dict(result), sort_keys=True, indent=2))

    # print(json.dumps(add_act_value_to_validate_dict(validate, result), sort_keys=True, indent=2))

    # convert_str_to_hump("check_version")
    # print(convert_str_to_hump("areaStatus"))

    pass
