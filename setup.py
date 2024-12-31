# setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code-analyzer",  # Project name
    version="1.0.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A local-hosted application for analyzing public/private repos or local projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steven-reyes/code-analyzer",
    packages=setuptools.find_packages(),
    include_package_data=True,  # If you want to include non-code files from MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask==2.2.5",
        "requests==2.31.0",
        # etc...
    ],
    entry_points={
        "console_scripts": [
            # Example: 'code-analyzer=src.main:main' to create a CLI named 'code-analyzer'
            "code-analyzer=src.main:main"
        ],
    },
)
