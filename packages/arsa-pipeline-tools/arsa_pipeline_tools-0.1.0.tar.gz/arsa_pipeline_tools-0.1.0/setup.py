from setuptools import setup, find_packages

setup(
    name="arsa-pipeline-tools",
    version="0.1.0",
    description="Utilities for Vertex AI pipelines, including GCS file management and dynamic module loading.",
    author="Harshit S",
    author_email="hrs19.pypi@gmail.com",
    url="https://github.com/hrs19/arsa-pipeline-tools",
    packages=find_packages(),
    install_requires=[
        "google-cloud-storage>=2.18.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
