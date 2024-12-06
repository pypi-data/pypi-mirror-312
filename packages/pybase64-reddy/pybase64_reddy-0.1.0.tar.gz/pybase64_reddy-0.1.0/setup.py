# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pybase64_reddy",  # Updated package name
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple base64 encode/decode tool with a CLI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pybase64_reddy",  # Update URL accordingly
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pybase64_reddy=pybase64_reddy.cli:main',
        ],
    },
    include_package_data=True,
)
