from setuptools import setup, find_packages

setup(
    name="tsax",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "None",
    ],
    entry_points={
        "console_scripts": [
            "tsax = tsax.downloader:download_file",
        ],
    },
    python_requires=">=3.6",
)
