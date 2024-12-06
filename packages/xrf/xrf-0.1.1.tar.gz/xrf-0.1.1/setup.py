import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xrf",
    version="0.1.1",
    author="Henrik Boström",
    author_email="bostromh@kth.se",
    description="ExPLAINABLE rANDOM fORESTS (xrf)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henrikbostrom/xrf",
    project_urls={
        "Bug Tracker": "https://github.com//henrikbostrom/xrf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["numpy", "pandas", "scikit-learn", "scipy", "joblib"],
    python_requires=">=3.8",
)
