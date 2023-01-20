from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]
setup(
    name="FHIRkit",
    version="0.0.30",
    description="Toolkit to handle FHIR Resources in a more efficient, pythonic way.",
    long_description=open("README.md").read(),
    url="",
    author="",
    author_email="",
    license="MIT",
    classifiers=classifiers,
    keywords="",
    packages=find_packages(),
    install_requires=["pydantic", "requests", "tqdm"],
)
