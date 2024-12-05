"""
未加密的tfduck/setup.py的代码
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tga-safe-oper-bsd",
    version="0.1.1",
    author="yuanxiao",
    author_email="yuan6785@163.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    # 需要安装的依赖
    install_requires=["ezconfig-client==0.7"],
    python_requires=">=3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=[],
)
