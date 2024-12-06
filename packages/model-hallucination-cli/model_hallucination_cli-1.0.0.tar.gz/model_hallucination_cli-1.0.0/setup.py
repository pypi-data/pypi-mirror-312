from setuptools import setup, find_packages


setup(
    name="model-hallucination-cli",
    version="1.0.0",
    author="Abhijit",
    description="A CLI for checking model hallucinations using Hugging Face datasets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abhijit/model-hallucination-cli",
    packages=find_packages(),
    install_requires=[
        "typer",
        "datasets",
        "rich",
        "numpy>=1.21.0,<1.22.0"
    ],
    entry_points={
        "console_scripts": [
            "model-hallucination=model_hallucination.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
