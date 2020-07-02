### 该目录存放的两个文件为备份文件。

environment.properties：用于将信息添加到Environment小部件内
Categories.json       ：自定义缺陷分类

这两个文件应该放在 allure report 目录下才能生效，由于名字太长，创建的时候很麻烦，就存放起来～


以下是官方文档给出的解释

4.2. Environment
To add information to Environment widget just create environment.properties (or environment.xml) file to allure-results directory before report generation.

environment.properties
```xml
Browser=Chrome
Browser.Version=63.0
Stand=Production
environment.xml
<environment>
    <parameter>
        <key>Browser</key>
        <value>Chrome</value>
    </parameter>
    <parameter>
        <key>Browser.Version</key>
        <value>63.0</value>
    </parameter>
    <parameter>
        <key>Stand</key>
        <value>Production</value>
    </parameter>
</environment>
```

4.3. Categories
There are two categories of defects by default:

Product defects (failed tests)

Test defects (broken tests)

To create custom defects classification add categories.json file to allure-results directory before report generation.

categories.json
[
  {
    "name": "Ignored tests", 
    "matchedStatuses": ["skipped"] 
  },
  {
    "name": "Infrastructure problems",
    "matchedStatuses": ["broken", "failed"],
    "messageRegex": ".*bye-bye.*" 
  },
  {
    "name": "Outdated tests",
    "matchedStatuses": ["broken"],
    "traceRegex": ".*FileNotFoundException.*" 
  },
  {
    "name": "Product defects",
    "matchedStatuses": ["failed"]
  },
  {
    "name": "Test defects",
    "matchedStatuses": ["broken"]
  }
]
(mandatory) category name
(optional) list of suitable test statuses. Default ["failed", "broken", "passed", "skipped", "unknown"]
(optional) regex pattern to check test error message. Default ".*"
(optional) regex pattern to check stack trace. Default ".*"
Test result falls into the category if its status is in the list and both error message and stack trace match the pattern.

categories.json file can be stored in test resources directory in case of using allure-maven or allure-gradle plugins.
