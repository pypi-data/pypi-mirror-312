from setuptools import setup, find_packages

setup(
    name="reqcurl",
    version="0.1.0",
    description="A Python wrapper for requests that parses cURL commands",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sufiyan Ali Iqbal",
    author_email="sufiyanaliiqbal@gmail.com",
    url="https://github.com/your_username/reqcurl",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
