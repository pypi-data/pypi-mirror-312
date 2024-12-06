from setuptools import setup, find_packages

setup(
    name="net-analysis",
    version="1.0.1",
    description="A package for analyze you IP and fetch additional information like ISP and LAT-LON, CITY, COUNTRY, etc",
    author="Sina",
    author_email="sinaorojlo53@gmail.com",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
