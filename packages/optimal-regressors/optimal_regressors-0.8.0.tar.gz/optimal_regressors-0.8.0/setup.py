from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="optimal-regressors",  
    version="0.8.0",  
    author="Rehan Taneja",
    author_email="rehan.taneja4321@gmail.com",
    description="A Python library to find optimal configurations for regressors",
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    url="https://github.com/RehanTaneja/OptimalRegressors.git",  
    packages=["OptimalRegressor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "scikit-learn",  
        "xgboost",
    ],
)
