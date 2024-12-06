from setuptools import setup, find_packages

setup(
    name="model-comparator",
    version="1.0.1",
    author="Abdallah Nassur",
    author_email="nassur1607@gmail.com",
    description="Une bibliothèque Python pour comparer différents modèles d'ajustement de données.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NassAbd/adjust_comparator",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "scikit-learn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
