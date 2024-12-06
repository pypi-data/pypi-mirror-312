from setuptools import setup, find_packages

setup(
    name="apache-airflow-providers-edge",
    version="2.10.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Apache Airflow Edge Provider",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apache-airflow-providers-edge",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)