from setuptools import setup, find_packages

setup(
    name="commit-checker",
    version="0.1.0",
    description="CLI tool to check your daily GitHub and local commits",
    author="Amariah Kamau",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "commit-checker = commit_checker.cli:main"
        ],
    },
    python_requires=">=3.7",
)
