#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/19 下午1:49
# @Author  : 周梦泽
# @File    : setup.py
# @Software: PyCharm
# @Description:STM32-ST-link的元数据

from setuptools import setup, find_packages

setup(
    name="STM32-ST-link",  # 包名，PyPI 上唯一
    version="1.1.0",  # 版本号
    author="Mason Zhou",  # 作者名
    author_email="qq2087698086@gmail.com",  # 作者邮箱
    description="STM32 ST-Link CLI microcontroller operations: connect, program, and erase. Before use, STM32 ST-LINK "
                "Utility must be installed.",  # 简短描述

    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",  # 详细描述的格式
    url="https://github.com/Mason-mengze/STM32_ST-link",  # 项目主页
    packages=find_packages(),  # 自动找到包
    zip_sage=False,
    include_package_data=True,  # 打包包含静态文件标识
    package_data={
        # 在包内包含特定的静态文件
        "STM32_ST_link": ["ST_Link_CLI/**/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
