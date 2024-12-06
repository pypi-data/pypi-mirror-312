from setuptools import setup, find_packages

setup(
    name="kubling_sqlalchemy",
    version="24.5.4",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4",
        "psycopg2-binary",
    ],
    entry_points={
        "sqlalchemy.dialects": [
            "kubling = kubling.dialect:KublingDialect",
        ]
    },
)