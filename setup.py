from setuptools import setup, find_packages
from setuptools.extension import Extension
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    from Cython.Build import cythonize
except:
    install("cython")
    from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

extensions = [
    Extension(
        "pyplumber.*",
        ["pyplumber/*.py"],
    ),
]

setup(
    name="pyplumber",
    version="0.1.9",
    license="GPL-3.0",
    description="PyPlumber provides some tools for looping pipelines using tasks and daemonized jobs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Gabriel Gazola Milan",
    author_email="gabriel.gazola@poli.ufrj.br",
    url="https://github.com/gabriel-milan/pyplumber",
    keywords=[
        "framework",
        "shared resources",
        "flexibility",
        "python",
        "online",
        "pipelines",
    ],
    install_requires=[
        "cython",
        "dill",
        "networkx",
        "redis",
        "typing",
    ],
    extras_require={
        "test": [
            "matplotlib",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
)