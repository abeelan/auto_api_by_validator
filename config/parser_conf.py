import os
from configparser import ConfigParser


class Config:

    def __init__(self, path):
        self.path = path
        self.config = ConfigParser()
        self.config.read(self.path, encoding='utf-8')

        if not os.path.exists(self.path):
            raise FileNotFoundError("请确保配置文件存在！")

    def get_sections(self):
        """ 得到所有的section，并以列表的形式返回

        :return
        list:
            ['section1', 'section2']
        """
        return self.config.sections()

    def get_options(self, section):
        """ 得到该section的所有option

        :return
        list:
            ['option1', 'option2']
        """
        return self.config.options(section)

    def get_section_items(self, section):
        """ 得到该section的所有键值对

        :return
            dict:
                {
                    ('option1': 'value1'),
                    ('option2': 'value2')
                }
        """
        return self.config.items(section)

    def get_value(self, section, option):
        """ 读取section中的option的值

        usage:
            get_value("section", "option")
        :return
            value
        """
        return self.config[section][option]

    def set_value(self, section, option, value):
        self.config.set(section, option, value)
        with open(self.path, "w+") as f:
            return self.config.write(f)

    def add_section(self, title):
        self.config.add_section(title)
        with open(self.path, "w+") as f:
            return self.config.write(f)


if __name__ == '__main__':
    pass

