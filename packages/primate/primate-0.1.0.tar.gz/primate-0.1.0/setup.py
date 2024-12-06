from setuptools import setup, find_packages

setup(
    name="primate",
    version="0.1.0",
    description="Primate AI: Decision-making and NLP tools inspired by " +
                "intelligent behavior.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/markdown",
    author="Primate",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "matplotlib",
    ],
)
