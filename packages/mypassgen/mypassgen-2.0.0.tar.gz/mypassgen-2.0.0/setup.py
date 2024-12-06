from setuptools import setup, find_packages

setup(
    name="mypassgen",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        # List any dependencies here
    ],
    author="Anup Ghosh",
    author_email="anupbsmrstu@gmail.com",
    description="An example of a custom library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)