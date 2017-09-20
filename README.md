# ITS SPIDER

## 1.安装

1. 安装**python3**
1. 安装**pip**:

    1. 下载[ez_setup.py](https://bootstrap.pypa.io/ez_setup.py)

    1. 用python 运行下载的ez_setup.py即可安装pip

1. 安装**requests**库: 在cmd中运行`pip install requests`

## 2.配置

配置**configure.json**:

    "time":抓取信息的间隔
    "email": 发送更新消息的邮箱
    "password": ITS的密码
    "username": ITS的帐户名

## 3.运行

命令行中运行: `python3 main.py`

## TODO:1.扩展本地求购和新闻频道