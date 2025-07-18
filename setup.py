from setuptools import setup, find_packages

setup(
    name="commit-checker",
    version="0.4.1",
    description="CLI tool to check your daily GitHub and local commits with advanced repository analytics",
    author="Amariah Kamau",
    packages=find_packages(),
    install_requires=["requests", "colorama", "packaging"],
    entry_points={
        "console_scripts": [
            "commit-checker = commit_checker.cli:main"
        ],
    },
    python_requires=">=3.7",
)
