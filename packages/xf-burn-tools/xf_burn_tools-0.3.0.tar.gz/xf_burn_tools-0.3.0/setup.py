#!/usr/bin/env python3

from setuptools import setup, find_packages
import xf_burn_tools

setup(
    name='xf_burn_tools',
    version=xf_burn_tools.__version__,
    author='kirto',
    author_email='sky.kirto@qq.com',
    description="A tools for Burn",
    packages=find_packages(),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache License 2.0", 
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # 项目状态
        "Intended Audience :: Developers",  # 目标受众
        "License :: OSI Approved :: Apache Software License",  # 指定使用 Apache 2.0
        "Programming Language :: Python",  # 支持的编程语言
        "Programming Language :: Python :: 3",  # Python 3 兼容
        "Programming Language :: Python :: 3.7",  # 具体支持的 Python 版本
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.6',
    install_requires=[
        'click',
        'pyserial',
    ],
    entry_points='''
        [console_scripts]
        burn=xf_burn_tools.burn_tools:FlashFirmware
    ''',
    include_package_data=True,
    package_data={
        # 指定需要打包的额外文件
        "": ["LICENSE", "README.md"],
    },
    data_files=[("", ["LICENSE"])],
)
