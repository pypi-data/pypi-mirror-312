from setuptools import setup, find_packages

setup(
    name="cash_optimizer",  # Replace with your package name
    version="0.1.0",  # Initial release version
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Replace with your repo URL
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",  # Replace with your license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],  # List of dependencies, e.g., ['numpy', 'requests']
)