import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyBingTiles",
    version="0.0.1",
    install_requires=[
        "pandas",
        "geopandas",
        "numpy",
        "shapely",
        "contextily"
    ],
    author="Shoichi Yip",
    author_email="shoichi.yip@gmail.com",
    description="A little tool in order to deal with Bing Tiles and to generate Shapefiles from them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shoyip/pybingtiles",
    project_urls={
        "Bug Tracker": "https://github.com/shoyip/pybingtiles/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
