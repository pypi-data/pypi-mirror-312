import setuptools
import os

# Get the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Read the contents of README.md for the long_description
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()
        
setuptools.setup(
    name="mostafamatrix",
    version="1.0.0",
    author="Mostafa Abotaleb",
    author_email="abotalebmostafa@bk.ru",
    description=(
        "A Python library for modeling univariate time series using the "
        "Generalized Least Deviation Method (GLDM) first order."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensures proper rendering on PyPI
    url="https://github.com/abotalebmostafa11/GLDMHO",  # Pointing to the repository root
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",  # Added additional Python versions
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",  # Explicitly specifying the license
    python_requires='>=3.6',  # Specify the Python versions you support
    install_requires=[
        # List your project dependencies here
        # Example:
        # "numpy>=1.18.0",
        # "pandas>=1.0.0",
    ],
    project_urls={  # Optional: Additional links
        "Bug Reports": "https://github.com/abotalebmostafa11/GLDMHO/issues",
        "Source": "https://github.com/abotalebmostafa11/GLDMHO",
    },
)
