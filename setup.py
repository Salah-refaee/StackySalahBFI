from setuptools import setup, find_packages
from sbfi import VERSION

setup(
    name="SBFI",
    version=VERSION,
    author="Salah Rami Al-Refaai",
    author_email="salah.alrerae@gmail.com",
    description="a simple and open-source BrainF**k interpreter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Salah2PLS/SalahBFI/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android/Linux, Any",
    ],
    python_requires=">=3.7",
    scripts=["scripts/sbfi"]
)
