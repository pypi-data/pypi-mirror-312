from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # Package name - this is what users will pip install
    name="aws-hotel-helpers",
    
    # Start with version 0.1.0 for initial release
    version="0.3.1",
    
    # Your information
    author="Your Name",
    author_email="your.email@example.com",
    
    # Short description that appears on PyPI
    description="AWS helper utilities for hotel management systems",
    
    # Long description from README.md
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Your project's homepage (e.g., GitHub repository)
    url="https://github.com/yourusername/aws-hotel-helpers",
    
    # Find all packages automatically
    packages=find_packages(),
    
    # Package classifiers - help users find your package
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    
    # Minimum Python version required
    python_requires=">=3.7",
    
    # Required dependencies
    install_requires=[
        "boto3==1.35.57",  # Match AWS CLI version
        "botocore==1.35.57",  # Match AWS CLI version
        "docutils>=0.16,<0.17"  # Compatible with AWS CLI
    ],
)