import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xhd_source",
    version="0.0.6",
    author="Hedi Xia",
    author_email="xiahedi@gmail.com",
    description="N/A",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hedixia/xhd_source",
    project_urls={
        "Bug Tracker": "https://github.com/hedixia/xhd_source/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)