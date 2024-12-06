# encoding: utf-8
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lane.chang on '07/07/2024'
    comment: 版本配置信息
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="laner",  # 模块名称
    version="1.3.3",  # 当前版本
    author="lane",  # 作者
    author_email="changlei-886@163.com",  # 作者邮箱
    description="一个非常实用的包",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/wupeiqi/fucker",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'pydantic',
    ],
    python_requires='>=3.9.0',
)
