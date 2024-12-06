from setuptools import find_packages, setup


def read_requirements(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line and not line.startswith("#")]


setup(
    name="mastermind-ai",
    version="1.6.2-beta",
    author="FlysonBot",
    author_email="FlysonBot@users.noreply.github.com",
    description="A Python package that simulates the Mastermind game with an AI solver.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FlysonBot/Mastermind",
    project_urls={
        "Repository": "https://github.com/FlysonBot/Mastermind",
        "Documentation": "https://flysonbot.github.io/Mastermind/",
        "Issues and Bugs": "https://github.com/FlysonBot/Mastermind/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Natural Language :: English",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements("src/requirements.txt"),
    entry_points={
        "console_scripts": [
            "mastermind = mastermind.main.main:main",
        ],
    },
)
