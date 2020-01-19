import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'sperch-aglensmith',
    version = '0.0.1',
    author="Austin Smith",
    author_email="aglensmith@gmail.com",
    description="Recursively search for swagger and openapi files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'sperch=sperch.__main__:main'
        ]

    },
    data_files = [('config', ['sperch/sperch.yaml'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )