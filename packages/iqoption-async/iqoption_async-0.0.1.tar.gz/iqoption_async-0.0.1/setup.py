from setuptools import setup, find_packages

setup(
    name="iqoption-async",
    version="0.0.1",
    description="An updated Python library for interacting with IQ Option using asyncio and modern WebSockets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Victor Rivera",
    author_email="victor.riverac92@gmail.com",
    url="https://github.com/s00rk/iqoption_async",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="iqoption trading api asyncio websockets"
)
