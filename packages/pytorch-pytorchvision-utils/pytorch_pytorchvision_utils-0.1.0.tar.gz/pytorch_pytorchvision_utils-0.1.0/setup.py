from setuptools import setup, find_packages

setup(
    name="pytorch-pytorchvision-utils",
    version="0.1.0",
    description="A simple PyTorch utility library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="yumingchang",
    author_email="yumingchang9527@gmail.com",
    url="https://github.com/YuMingCorn/torch-utils",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
