from setuptools import setup, find_packages

setup(
    name="UniversalBackupValidator",  # Package name
    version="1.0.0",  # Initial version
    author="tudos4",
    author_email="your_email@example.com",  # Replace with your email
    description="A tool for validating and verifying backup files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tudos4/UniversalBackupValidator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "colorama>=0.4.4",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ubv=UniversalBackupValidator.cli:main",  # Shortcut command for CLI usage
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

