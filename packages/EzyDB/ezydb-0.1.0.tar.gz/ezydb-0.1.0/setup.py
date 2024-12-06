
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EzyDB",
    version="0.1.0",
    description="EzyDB is a lightweight, file-based NoSQL database system designed for Python developers.",
    author="Rakesh Kanna",
    author_email='rakeshkanna0108@gmail.com',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['database', 'db', 'nosql', 'json', 'bson', 'storage', 'store'],
    install_requires=
        [],
    entry_points={"console_scripts":["ezydb = ezydb:main"]}
)
