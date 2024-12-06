from setuptools import setup, find_packages

setup(
    name="godx",  # Replace with your CLI tool name
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "requests",  # Dependencies
    ],
    entry_points={
        "console_scripts": [
            "godx=godx.godx:main",  # Define the command and entry point
        ],
    },
    author="Ghost",
    description="God Written By Ghost",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
