from setuptools import setup, find_packages

setup(
    name="openup",
    author="Scott Beddall",
    author_email="sbeddall@gmail.com",
    url="https://github.com/semick-dev/fbi-open-up",
    description="The local interface to interact with the fbi agent process.",
    version="0.1.0",
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
        "requests"
        "azure-storage-blob>="
    ],
    entry_points={
        "console_scripts": [
            "fbi=fbi:main",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)