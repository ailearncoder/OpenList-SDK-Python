"""
OpenList API Python客户端库的安装配置
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="openlist-api",
    version="1.0.0",
    author="OpenList API Contributors",
    author_email="",
    description="一个功能完整的Python客户端库，用于与OpenList (AList) API进行交互",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openlist_api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="openlist alist api client file-management cloud-storage",
    project_urls={
        "Documentation": "https://github.com/yourusername/openlist_api",
        "Source": "https://github.com/yourusername/openlist_api",
        "Bug Reports": "https://github.com/yourusername/openlist_api/issues",
    },
)
