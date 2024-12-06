from setuptools import setup, find_packages

setup(
    name="EDS-Lib",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
    ],
    author="mk-samoilov",
    author_email="maksim.samoilov.0202@gmail.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mk-samoilov/EDS-Python-Lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)