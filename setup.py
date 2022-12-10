import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dohome_api",
    version="0.1.1",
    author="Mikhael Khrustik",
    description="Library for controlling smart bulbs that are controlled by the DoIT protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'dohome_api',
        'dohome_api.light',
        'dohome_api.datagram',
        'dohome_api.transport',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'aiodatagram==0.0.1',
        'arrrgs==0.0.2'
    ],
    python_requires='>=3.7',
    package_dir={'':'.'},
)
