import os


def project_path():
    return os.path.dirname(os.path.dirname(__file__))


def case_path():
    return "".join([project_path(), "/case"])


def yaml_path():
    return "".join([project_path(), "/har2yaml"])


def report_path():
    return "".join([project_path(), "/report"])


def config_path():
    return "".join([project_path(), "/config"])


if __name__ == '__main__':
    print(config_path())
