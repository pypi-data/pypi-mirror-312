from setuptools import setup, find_packages

setup(
    name="britishairways",
    version="0.1.1",
    description="A Python package for fetching British Airways flight prices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Alex Choi",
    author_email="alexchoidev@gmail.com", 
    url="https://github.com/alexechoi/british-airways-py",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)