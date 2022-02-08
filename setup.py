from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
setup(
    name="",
    version="0.0.1",
    description="Utils to handle FHIR Terminology Resources more efficiently",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="",
    author="",
    author_email="",
    license="MIT",
    classifiers=classifiers,
    keywords="",
    packages=find_packages(),
)
