from setuptools import setup, find_packages

setup(
    name="biddmanager_pkg",
    version="0.1.0",
    author="rahul shirsat",
    author_email="rahulshirsat9156@gmail.com",
    description="this libarbary is for managing the bids of user ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_repository",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
