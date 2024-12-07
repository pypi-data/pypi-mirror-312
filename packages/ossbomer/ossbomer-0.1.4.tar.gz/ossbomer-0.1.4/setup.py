from setuptools import setup, find_packages
import os

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "ossbomer", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Version not found in __init__.py")

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ossbomer",
    version=get_version(),
    description="SBOMs quality validator for Open Source License Compliance.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author="Oscar Valenzuela",
    author_email="oscar.valenzuela.b@gmail.com",
    license='Apache 2.0',
    url='https://github.com/Xpertians/xmonkey-ossbomer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "jsonschema",
        "requests",
        "PyYAML",
        "tqdm"
    ],
    package_data={
        "ossbomer": [
            "datasets/*.json",
            "datasets/package_signatures/*.json"
        ]
    },
    entry_points={
        "console_scripts": [
            "ossbomer=ossbomer.cli:main",
        ],
    },
    python_requires='>=3.6',
)
