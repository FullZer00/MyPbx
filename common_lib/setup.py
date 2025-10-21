from setuptools import setup, find_packages

setup(
    name="common-lib",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pydantic>=2.0.0",
        "dotenv",
        "pydantic-settings>=2.11.0",
        "python-json-logger>=2.0.0",
    ],
)