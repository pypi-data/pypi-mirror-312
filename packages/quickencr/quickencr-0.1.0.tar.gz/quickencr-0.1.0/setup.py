from setuptools import setup, find_packages

setup(
    name="quickencr",
    version="0.1.0",
    description="A simple library for encrypting and decrypting text and files.",
    author="Avishek Agarwla",
    author_email="avigreat29@gmail.com.com",
    url="https://github.com/Avi-29/quickEncrypt.git",  # Update with your repository URL
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.3",  # Dependency for encryption
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
