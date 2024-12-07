from setuptools import setup, find_packages

setup(
    name="secfi",  
    version="0.1.0",
    description=" Python tool to collect SEC filings for all publicly traded companies. Easily fetch forms like 10-K, 10-Q, and 8-K, along with links and document contents. Ideal for analysts, researchers, and anyone exploring financial reports or SEC data. Simplify your access to essential company information",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Juan Pablo Pisano",
    author_email="pisanojuanpablo@gmail.com",
    url="https://github.com/gauss314/secfi",
    license="MIT",
    packages=find_packages(), 
    install_requires=[], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
