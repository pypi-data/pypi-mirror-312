# setup.py

from setuptools import setup, find_packages

setup(
    name="atari-monk-cli-tool",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "am_cli_tool = cli_tool.main:main",
        ],
        "cli_tool.commands": [
            "basic_commands = cli_tool.basic_commands:load",
        ],
    },
    install_requires=["atari-monk-cli-logger", "atari-monk-keyval-storage", "atari-monk-cli-tool-commands"],
    description="A modular CLI application that supports dynamic command sets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="atari monk",
    author_email="atari.monk1@gmail.com",
    url="https://github.com/atari-monk/cli_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12.0",
)
