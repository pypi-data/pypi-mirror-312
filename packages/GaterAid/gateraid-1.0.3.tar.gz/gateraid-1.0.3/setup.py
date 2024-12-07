from setuptools import setup, find_packages  # noqa: D100

setup(
    name="GaterAid",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[
        "numpy >= 2.0.0",
    ],
    author="Eleanor Kneip, Stasiu Wolanski, Joel the intern",
    author_email="eleanor.kneip.24@ucl.ac.uk, \
        stanislaw.wolanski.24@ucl.ac.uk, joel.mills.24@ucl.ac.uk",
    description="A package to abate the strait of applying a two-qubit gate \
        to a quantum state.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://statuesque-smakager-de86a9.netlify.app",  # or whatever URL you end up using
        "Source": "https://github.com/QC2-python-SE/QWACOBEC",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
