from setuptools import setup, find_packages

setup(
    name="sxtg",
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.11",
    description="aiogram util.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="A2RK",
    author_email="atwork.igor@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )
