from setuptools import setup, find_packages

setup(
    name="fbiopenup",
    author="Scott Beddall",
    author_email="sbeddall@gmail.com",
    url="https://github.com/semick-dev/fbi-open-up",
    description="A combined local interface and agent process that enables remote debugging of devops agents.",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    install_requires=["setuptools>=45.0", "requests", "azure-storage-queue>=12.3.0", "colorama"],
    entry_points={"console_scripts": ["openup=fbi.openup:main", "fbi=fbi.fbi:main", "fbi_reset=fbi:reset"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)
