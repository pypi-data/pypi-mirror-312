from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="math_ops_viviani",
    version="0.0.1",
    author="Viviani Pedroso",
    author_email="viani22@gmail.com",
    description="The package math_operations",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vivianikelly/math-operations-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)