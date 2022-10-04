from setuptools import setup, find_packages

setup(
    name="kakao.py",
    version="0.3.0",
    url="https://github.com/jhleekr/kakao.py",
    author="jhleekr",
    author_email="jhlee@bfy.kr",
    description="Very simple kakaotalk LOCO/HTTP API protocol wrapper for python.",
    packages=["kakao", "kakao.ext", "kakao.ext.commands"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["pymongo", "requests", "pycryptodomex"],
    zip_safe=False,
    classifiers=["License :: OSI Approved :: MIT License"],
)
