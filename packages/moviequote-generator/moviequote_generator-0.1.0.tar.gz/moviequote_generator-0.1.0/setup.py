from setuptools import setup, find_packages

setup(
    name="moviequote_generator",  # Replace with your library name
    version="0.1.0",
    author="Albin Biju",
    author_email="alby7370@gmail.com",
    description="This is random movie quote generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alby2255/moviequote_generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
