from setuptools import setup, find_packages

setup(
    name="commit-checker",
    version="0.7.5",
    description="AI-powered commit mentor CLI tool with Wisdom Drop integration, contextual commit suggestions, smart profile system, advanced analytics, and TIL logging",
    author="Amariah Kamau",
    packages=find_packages(),
    install_requires=["requests", "colorama", "packaging", "textual", "plotext", "markdown"],
    extras_require={
        "ai": ["transformers", "torch"]
    },
    entry_points={
        "console_scripts": [
            "commit-checker = commit_checker.cli:main"
        ],
    },
    python_requires=">=3.13",
)
