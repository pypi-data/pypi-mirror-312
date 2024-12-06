from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moviequote_generator",  # Replace with your library name
    version="0.2.0",
    author="Albin Biju",
    author_email="alby7370@gmail.com",
    description="This is a movie quote generator",
    long_description=long_description,
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
