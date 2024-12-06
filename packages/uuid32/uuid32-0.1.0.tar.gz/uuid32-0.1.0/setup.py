from setuptools import setup, find_packages

setup(
    name="uuid32",
    version="0.1.0",
    description="A library to generate 32-character random strings using digits and lowercase letters.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/balyakin/uuid32",
    author="Evgeny Balyakin",
    author_email="jkwork@yandex.ru",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
