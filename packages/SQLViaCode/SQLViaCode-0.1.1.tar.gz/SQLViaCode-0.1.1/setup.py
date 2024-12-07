from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="SQLViaCode",
    version="0.1.1",
    description="A Python package to query SQL databases and manage backups.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Afik Ratzon",
    author_email="afik.ratzon@gmail.com",
    packages=find_packages(),
    install_requires=requirements,  # Use the list from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
