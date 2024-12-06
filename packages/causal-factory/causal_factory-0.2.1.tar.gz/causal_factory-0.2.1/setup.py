from setuptools import setup, find_packages

setup(
    name="causal-factory",
    version="0.2.1",  # Increment the version for the new release
    description="CausalFactory is Python package for causal model discovery and inference aims to seamlessly discover, visualize, and operationalize causal relationships",
    long_description="CausalFactory is Python package for causal model discovery and inference aims to seamlessly discover, visualize, and operationalize causal relationships",  # Ensure you have a README.md file
    long_description_content_type="text/markdown",
    author="Awadelrahman M. A. Ahmed",
    author_email="awadrahman@gmail.com",
    url="https://github.com/Awadelrahman/causal-factory",  # Update if needed
    packages=find_packages(),  # Automatically find and include all packages/modules
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
    "mlflow",  
    "pandas",
    "gastle",  # Ensure you spell this correctly or replace with "castle"
    "torch",
    "numpy",  # Add numpy
    "networkx",  # Add networkx
    "matplotlib",  # Add matplotlib
],
)
