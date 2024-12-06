from setuptools import setup, find_packages

# 读取 README 文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ipm-python",  # 包名称
    version="1.3.alpha7",  # 初始版本号
    author="IngotStudio",  # 作者名称
    author_email="xmz_20130612@163.com",  # 作者邮箱
    description="A simple Python package manager like pip.",  # 简短描述
    long_description=long_description,  # 长描述，读取自 README 文件
    long_description_content_type="text/markdown",  # 长描述格式
    url="https://github.com/your-repo/ipm-python",  # 项目主页
    project_urls={  # 项目相关链接
        "Bug Tracker": "https://github.com/your-repo/ipm-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",  # 支持的编程语言
        "License :: OSI Approved :: MIT License",  # 使用的许可证
        "Operating System :: OS Independent",  # 操作系统独立
    ],
    package_dir={"": "ipm"},  # 包目录
    packages=find_packages(where="ipm-python"),  # 自动发现包
    python_requires=">=3.6",  # Python 版本要求
    install_requires=[
        "requests>=2.26.0",  # 依赖项
        "tqdm>=4.62.3",
        "beautifulsoup4>=4.10.0",
    ],
    entry_points={
        "console_scripts": [
            "ipm=ipm_cli:main",  # 命令行入口，`ipm` 对应 `ipm_cli.py` 的 `main` 方法
        ],
    },
)
