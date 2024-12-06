from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="x_lolo",
    version="0.1.0",
    author="lolo skiiii",
    author_email="uha22211@gmail.com",
    description="A Python library for direct interaction with Twitter's unofficial API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohaskii/x_lolo_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
)