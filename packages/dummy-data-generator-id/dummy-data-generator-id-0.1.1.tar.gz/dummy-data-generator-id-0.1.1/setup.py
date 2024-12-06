from setuptools import setup, find_packages

setup(
    name="dummy-data-generator-id",
    version="0.1.1",
    author="Brian Adi",
    author_email="uix.brianadi@gmail.com",
    description="A library for generating realistic dummy data for Indonesian context",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bri-anadi/dummy-data-generator-id",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'uuid'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    keywords="dummy-data generator indonesia random",
)
