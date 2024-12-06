from setuptools import setup, find_packages

setup(
    name="nasr_search",
    version="0.3.0",
    author="Eslam",
    author_email="eslam.mostafa000@gmail.com",
    description="Search for values in XLSX files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "openpyxl"],
    entry_points={
        "console_scripts": [
            "nasr_search=nasr_search.nasr_search:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
