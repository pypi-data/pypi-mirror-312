from setuptools import setup, find_packages

setup(
    name="qiscus-python-sdk",
    version="0.0.1",
    author="Rahmad Afandi",
    author_email="rahmadafandiii@gmail.com",
    description="Qiscus SDK for Python (sync and async client)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yomaaf/qiscus-python-sdk",
    packages=find_packages(where="qiscus_python_sdk"),
    install_requires=[
        "httpx",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
