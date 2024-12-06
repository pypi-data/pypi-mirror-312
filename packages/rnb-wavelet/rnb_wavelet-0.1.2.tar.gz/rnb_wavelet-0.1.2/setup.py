from setuptools import setup, find_packages


packages = find_packages()
print("Discovered packages:", packages)


setup(
    name="rnb-wavelet",
    version="0.1.2",
    description="rnb-Wavelet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Michael Foti",
    author_email="michael-christopher.foti.1@ens.etsmtl.ca",
    url="https://github.com/yourusername/rnb",
    packages=find_packages(),  # Automatically includes all submodules
    include_package_data=True,  # Ensures non-code files are included if specified
    package_data={
        'rnb':['data/*.npy'],
    },
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "statsmodels"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
