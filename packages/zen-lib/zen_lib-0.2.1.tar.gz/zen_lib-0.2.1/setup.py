# -*- coding:utf-8 -*-
import platform
requires = []
import setuptools
##with open("README.md", "r") as fh:
##    long_description = fh.read()
setuptools.setup(
    name="zen_lib", 
    version="0.2.1",
    author='lhyweb',
    install_requires=requires,
    author_email="lhyweb@gmail.com",
    keywords=[],
    description="""personal utilities code for esp32""",
##    long_description=long_description,
##    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
##    python_requires='>=3.6',
)
