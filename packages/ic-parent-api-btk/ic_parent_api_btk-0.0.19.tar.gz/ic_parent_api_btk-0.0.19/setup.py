import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="ic_parent_api_btk",
    version="0.0.19",
    author="Brian Keifer",
    author_email="brian@valinor.net",
    description="",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkeifer/ic_parent_api_btk",
    license="MIT",
    packages=setuptools.find_packages(
        'src',
        exclude=['__pycache__', 'venv']
    ),
    package_dir={'': 'src'},
    install_requires=[
        "aiohttp",
        "pydantic>=1.8.2,<1.13.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
