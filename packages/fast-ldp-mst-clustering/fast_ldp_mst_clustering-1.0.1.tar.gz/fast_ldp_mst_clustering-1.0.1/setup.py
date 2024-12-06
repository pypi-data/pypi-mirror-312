import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast_ldp_mst_clustering", 
    version="1.0.1", 
    author="Teng Qiu",
    author_email="qiutengcool@163.com",
    description="Fast_LDP_MST is an efficient density-based clustering method for large-size datasets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Teng-Qiu-Clustering/Fast-LDP-MST-Clustering-IEEE-TKDE-2022",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
