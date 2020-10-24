import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="janch-taarimalta", # Replace with your own username
    version="0.0.1",
    author="Sawan Vaidya",
    author_email="",
    description="A YAML config centric tool to act on your service status",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'Click',
    ],
    entry_points='''
    [console_scripts]
    janch=janch.cli:main
    '''
)
