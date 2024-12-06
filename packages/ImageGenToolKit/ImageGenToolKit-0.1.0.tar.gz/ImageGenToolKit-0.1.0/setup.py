from setuptools import setup, find_packages

setup(
    name="ImageGenToolKit",
    version="0.1.0",
    description="Asynchronous AI image generation library with proxy support.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Barot",
    author_email="turxonovbarot@gmail.com",
    url="https://github.com/BarotbekTurxonov/ImageGenToolKit",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.1",
        "fake_useragent",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
