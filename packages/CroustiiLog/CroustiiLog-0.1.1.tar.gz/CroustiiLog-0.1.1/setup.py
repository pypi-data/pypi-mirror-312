from setuptools import setup, find_packages

setup(
    name="CroustiiLog",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    description="A customizable logging package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="kebabou.r",
    author_email="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
 