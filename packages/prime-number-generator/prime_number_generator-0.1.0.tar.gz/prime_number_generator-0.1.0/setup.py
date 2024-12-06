from setuptools import setup, find_packages

setup(
    name="prime_num_generator",
    version="0.1.0",
    description="A utility package for prime number generation and operations",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)
