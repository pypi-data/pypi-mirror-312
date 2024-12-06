from setuptools import setup, find_packages

setup(
    name="atari-monk-cli-tool-commands",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "cli_tool.commands": [
            "custom_commands = cli_commands.custom_commands:load",
        ],
    },
    install_requires=["yt-dlp>=2023.3.1","pyperclip", "atari-monk-keyval-storage", "atari-monk-pytoolbox", "atari-monk-cli-logger", ""],
    description="A custom commands package for CLI Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="atari monk",
    author_email="atari.monk1@gmail.com",
    url="https://github.com/atari-monk/cli_commands",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12.0",
)
