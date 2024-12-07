from setuptools import setup, find_packages

setup(
    name="snowdaypredictor-API",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "selenium>=4.15.2",
        "pydantic>=2.5.1",
        "pydantic-settings>=2.1.0",
        "python-dotenv>=1.0.0",
        "httpx>=0.25.2",
    ],
    author="Rorello Development",
    author_email="rorellodevelopment@gmail.com",
    description="A Python package to predict snow day chances using snowdaypredictor.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Roreos/SnowDayPredictor-API",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 