from setuptools import setup, find_packages

setup(
    name="kyakx",
    version="1.1.1",
    author="kyakei",
    author_email="codtool911@gmail.com",
    description="A powerful web exploitation toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kyakei/kyakx",
    packages=find_packages(include=["kyakx", "kyakx.*"]),
    include_package_data=True,
    install_requires=[
        "colorama",
        "requests",
        "paramiko"
    ],
    entry_points={
        "console_scripts": [
            "kyakx=kyakx.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
