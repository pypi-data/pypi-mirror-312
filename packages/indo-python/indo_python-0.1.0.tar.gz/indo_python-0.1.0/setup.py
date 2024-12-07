from setuptools import setup, find_packages

setup(
    name="indo-python",         # Package name (should be unique)
    version="0.1.0",            # Version
    author="Your Name",         # Your name
    author_email="your_email@example.com",
    description="Overrides built-in Python functions with custom names.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/indo-python",  # GitHub repo URL
    packages=find_packages(),   # Automatically find subpackages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",    # Minimum Python version
)
