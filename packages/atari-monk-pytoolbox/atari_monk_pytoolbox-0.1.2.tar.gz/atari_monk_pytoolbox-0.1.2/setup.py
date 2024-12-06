from setuptools import setup, find_packages

setup(
    name="atari-monk-pytoolbox",
    version="0.1.2",
    packages=find_packages(),
    entry_points={},
    install_requires=["atari-monk-cli-logger"],
    description="A tools package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="atari monk",
    author_email="atari.monk1@gmail.com",
    url="https://github.com/atari-monk/pytoolbox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12.0",
)
