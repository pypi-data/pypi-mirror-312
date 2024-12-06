from setuptools import setup, find_packages

setup(
    name="BUILDER_ADDON_PCA",  # Replace with your project name
    version="0.0.1",  # Initial version
    author="e-matica",
    author_email="alessandro.robbiano@e-matica.it",
    description="PCA Package for Seeq Addons",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
