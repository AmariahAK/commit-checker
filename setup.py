from setuptools import setup, find_packages

setup(
    name="commit-checker",
    version="0.8.0",
    description="AI-powered commit mentor CLI tool with Wisdom Drop integration, VS Code extension support, gamification, smart profile system, advanced analytics, and TIL logging - now faster and more streamlined",
    author="Amariah Kamau",
    packages=find_packages(),
    install_requires=["requests", "colorama", "packaging", "textual", "plotext", "markdown"],
    extras_require={
        "ai": ["transformers>=4.30.0", "torch>=2.0.0"]
    },
    entry_points={
        "console_scripts": [
            "commit-checker = commit_checker.cli:main"
        ],
    },
    python_requires=">=3.13",
)
