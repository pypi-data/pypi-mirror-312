from setuptools import find_packages, setup

# Read the README file for long description
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="logafault",
    version="0.1.3",
    description="An SDK for interacting with CityPower's APIs.",
    # Package details
    package_dir={"": "logafault"},
    packages=find_packages(where="logafault"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cliftondhanee/logafault",
    author="Clifton Dhanee",
    author_email="clifton.dhanee@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    python_requires=">=3.9",
)
