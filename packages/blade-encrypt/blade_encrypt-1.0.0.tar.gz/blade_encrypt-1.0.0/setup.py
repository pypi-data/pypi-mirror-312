from setuptools import setup, find_packages

setup(
    name="blade-encrypt",
    version="1.0.0",
    description="BLADE Encryption and Compression Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DARKTRON",
    packages=find_packages(),
    install_requires=["cryptography","fade","colorama"],
    entry_points={
        "console_scripts": [
            "BLADE=blade.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
