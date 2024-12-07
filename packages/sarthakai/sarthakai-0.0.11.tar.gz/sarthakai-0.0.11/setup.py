from setuptools import setup, find_packages

with open("README.MD", "r") as f:
    readme_content = f.read()

setup(
    name="sarthakai",
    version="0.0.11",
    packages=find_packages(),
    long_description=readme_content,
    long_description_content_type="text/markdown",
    install_requires=[
        "litellm==1.49.0",
    ],
)
