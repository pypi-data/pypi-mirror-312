from setuptools import setup, find_packages

setup(
    name="niho",
    version="1.0.0",
    description="Niho is a simple HTTP server framework.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nihad Kerimli",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
