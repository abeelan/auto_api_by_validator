import os
import io
import yaml


def load_yaml(path):
    with open(path, 'r') as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content


def dump_yaml(content, yaml_file):
    with io.open(yaml_file, "w", encoding="utf-8") as outfile:
        yaml.dump(
            content,
            outfile,
            allow_unicode=True,  # 包含中文需要设置为 True，否则不会正常展示
            default_flow_style=False,  # 格式序列化
            indent=4  # 设置缩进
        )


if __name__ == '__main__':
    # _path = "./all_api.yml"
    # all_api = load_yaml(_path)
    pass
