from setuptools import setup, find_packages

setup(
    name="search_prompts",
    version="1.0.0",
    description="A package for searching prompts in Hugging Face datasets",
    author="MurlocLevel7",
    packages=find_packages(),
    install_requires=[
        "datasets"
    ],
    python_requires=">=3.7",
)
