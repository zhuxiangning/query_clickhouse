<p align="right"><font size="8" face="Times"><a href="./README.md">zh-cn</a> | <a href="../../../README.md">en-us</a></font></p>

# query_clickhouse
连接到clickhouse，并用sql从其中查询结果。

***



## 工程目录

包含3个最重要的文件夹:

1. etc/: 包含所有的配置和默认设置. 

   注: 'profile.py' 对隐私极其重要（推送代码时请慎重检查），其中包含了很多认证设置。'logging.json' 仅用于记录runtime日志信息。

2. data/: src ----经script处理----> result. Notes: 'src/' 与 'result/' 中的文件是一一对应的.

3. script/: 典型的 javaweb 目录(controller <------service<------utils).

![directory-structure](../../../stastic/images/directory-structure.png)

## Quick Start

1. 在 'profile.py' 中设置您的认证信息。

2. 修改 '/script/query_sql.py':

   2.1 在 [X-lab2017](https://github.com/X-lab2017)/**[github-analysis-report](https://github.com/X-lab2017/github-analysis-report)** 中克隆您的目标工程, 它可以是 'github-analysis-report/sql/' 或 'github-analysis-report/case-study/sql/' 的子目录。把克隆副本放入 'data/src/'。

   2.2 必要时修改 pre-process 和 post-processor。 ![script-query_sql-content](../../../stastic/images/script-query_sql-content.png)

3. 运行 'script/service/query_sql.py'。 在 'data/result' 查看运行结果。

## 相关链接

1. 相关项目：[X-lab2017/github-analysis-report](https://github.com/X-lab2017/github-analysis-report)

2. 相关公众号及推送文章：[重磅 |《GitHub 2020 数字洞察报告》正式发布](https://mp.weixin.qq.com/s/DYySsVe5Z2NH0hvGi4xlKg)

3. 相关资源：[《GitHub 2020 数字洞察报告》](http://oss.x-lab.info/github-insight-report-2020.pdf)

4. 实验室简介：[X-Lab](http://www.x-lab.info/)

说明：本项目[birdflyi/query_clickhouse](https://github.com/birdflyi/query_clickhouse)是项目[X-lab2017/github-analysis-report](https://github.com/X-lab2017/github-analysis-report)的关联项目。部分功能与[《GitHub 2020 数字洞察报告》](http://oss.x-lab.info/github-insight-report-2020.pdf)保持一致，简介见公众号相关推文：[重磅 |《GitHub 2020 数字洞察报告》正式发布](https://mp.weixin.qq.com/s/DYySsVe5Z2NH0hvGi4xlKg)。

