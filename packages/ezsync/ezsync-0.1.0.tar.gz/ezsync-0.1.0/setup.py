from setuptools import setup, find_packages

setup(
    name="ezsync",
    version="0.1.0",
    description="Simple syncing of python objects across websockets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Julie Ganeshan",
    author_email="HeavenlyQueen@outlook.com",
    url="https://github.com/Sanjay-Ganeshan/ezsync",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[],  # Add any dependencies here
)
