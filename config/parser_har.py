"""
解析 har 文件，获取预期数据类型
"""
import os
import io
import sys
import json
import logging
import base64

from common import convert


class ParamsHar:

    def __init__(self, file_path):
        """ Gets the entire contents of the entries in the har file

        Args:
            *.har(file)

        Return:
            <class 'dict'>
        """
        # TODO: 判断是否是har文件
        with io.open(file_path, "r+", encoding="utf-8-sig") as f:
            try:
                content_json = json.loads(f.read())
                self.content = content_json["log"]["entries"][0]
            except (KeyError, TypeError):
                logging.error("HAR file content error: {}".format(file_path))
                sys.exit(1)

    def get_request_content(self):
        return self.content["request"]

    def get_response_content(self):
        return self.content["response"]

    def get_method(self):
        return self.get_request_content()["method"]

    def get_cookies(self):
        return self.get_request_content()["cookies"]

    def get_request_headers(self):
        headers_dict = {}
        headers = self.get_request_content()["headers"]
        for header in headers:
            headers_dict[header["name"]] = header["value"]
        return headers_dict

    def get_params(self):
        params_dict = {}
        params = self.get_request_content()["queryString"]
        for param in params:
            params_dict[param["name"]] = param["value"]
        print(params_dict)

    def get_post_data(self):
        if self.get_method() in ["POST", "PUT", "PATCH"]:
            post_data = self.get_request_content().get("postData", {})
            mime_type = post_data.get("mimeType")

            # Note that text and params fields are mutually exclusive.
            if "text" in post_data:
                post_data = post_data.get("text")
            else:
                params = post_data.get("params", [])
                post_data = convert.convert_list_to_dict(params)

            if not mime_type:
                pass
            elif mime_type.startswith("application/json"):
                try:
                    # 异常处理：将文本转换为 dict，一般直接是 dict
                    post_data = json.loads(post_data)
                except json.decoder.JSONDecodeError:
                    # 触发该异常可忽略，预期中
                    pass

            elif mime_type.startswith("application/x-www-form-urlencoded"):
                post_data = convert.convert_data_form_to_dict(post_data)

            return post_data

    def get_response_cookies(self):
        return self.get_response_content()["cookies"]

    def get_response_headers(self):
        headers_dict = {}
        headers = self.get_response_content()["headers"]
        for header in headers:
            headers_dict[header["name"]] = header["value"]
        return headers_dict

    def get_response(self):
        response_content_dict = self.get_response_content()["content"]
        text = response_content_dict.get("text")
        if not text:
            return

        # 特殊处理 json 编码格式
        mime_type = response_content_dict.get("mimeType")
        if mime_type and mime_type.startswith("application/json"):
            encoding = response_content_dict.get("encoding")
            if encoding and encoding == "base64":
                content = base64.b64decode(text).decode("utf-8")
            else:
                content = text

            try:
                response_content_json = json.loads(content)
                if not isinstance(response_content_json, dict):
                    return
                return response_content_json
            except json.decoder.JSONDecodeError:
                logging.warning(
                    "response content can not be loaded as json: {}".format(content.encode("utf-8"))
                )
                return


if __name__ == '__main__':
    __path = os.path.dirname(os.path.dirname(__file__)) + "/har2yaml/loginByPhone.har"
    content = ParamsHar(__path)
    print(content.get_response())
    print(convert.convert_json_to_validate_dict(content.get_response()))
