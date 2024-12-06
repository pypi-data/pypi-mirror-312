from setuptools import setup, find_packages

setup(
    name="allsort",  # Your package name
    version="0.1.0",  # Version number (initial release)
    description="A Python package for sorting dictionaries, lists, tuples, and sets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Amit Ghatge",
    author_email="amitghatge37@gmail.com",
    url="https://github.com/Amit145/allsort",  # GitHub repository
    license="MIT",
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
