from setuptools import setup, find_packages

setup(
    name="git_branch_manager",
    version="0.1.0",
    author="Dhruba Dahal",
    author_email="dhruba.dahal03@gmail.com",
    description="A tool to manage Git branches across repositories.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DahalRocks/git_branch_manager",
    packages=find_packages(),
    install_requires=[
        "PyYAML>=6.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "git-branch-manager=git_branch_manager.main:main",
        ]
    },
)
