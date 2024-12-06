from setuptools import setup, find_packages

setup(
    name="causara",
    version="0.1.1",
    author="causara UG",
    author_email="support@causara.com",
    description="TODO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://causara.com",
    packages=find_packages(),
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9, <3.13",
    install_requires=[
        "numpy"
    ],
)
