import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="safe_dencrypt",
    version="0.2",
    author="Chenming Lai",
    author_email="18859950787@163.com",
    description="A lib to decrypt or encrypt message convinet and safe!expert!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kkgithub.com/ytsidle/safe-dencrypt",
    packages=setuptools.find_packages(),
    install_requires=[],

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)