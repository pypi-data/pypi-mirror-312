from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fakeinvoicegen",
    version="0.1.0",
    author="Khushal jethava",
    author_email="khushaljethava14@outlook.com",
    description="A package to generate fake invoices using Faker and InvoiceGenerator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Khushaljethava/fakeinvoicegen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Faker>=8.0.0",
        "InvoiceGenerator>=0.5.0",
    ],
)
