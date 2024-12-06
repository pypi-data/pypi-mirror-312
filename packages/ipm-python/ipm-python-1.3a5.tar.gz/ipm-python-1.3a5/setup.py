from setuptools import setup, find_packages

setup(
    name="ipm-python",
    version="1.3.alpha5",
    author="IngotStudio",
    author_email="xmz20130612@163.com",
    description="改进版 Python 软件包管理器，支持国内镜像和动态进度条。",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/IngotStudio/ipm-python",
    packages=find_packages(),
    install_requires=[
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "ipm=ipm.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
