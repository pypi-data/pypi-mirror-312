from setuptools import setup, find_packages

setup(
    name="cognidb",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "mysql-connector-python",
        "openai",
        "sqlparse"
    ],
    author="Rishabh Kumar",
    author_email="rishabh.vaaiv@gmail.com",
    description="A tool for generating SQL queries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/boxed-dev/cognidb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
