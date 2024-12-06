from setuptools import setup, find_packages

setup(
    name="phishing-detection-py",
    version="0.1.0",
    description="A library for phishing detection using Hugging Face models.",
    author="cmacha2",
    author_email="cristiancmg127@gmail.com",
    url="https://github.com/cmacha2/phishing-detection-py",
    license="Apache 2.0",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "scikit-learn",
        "pandas",
        "numpy",
        "imblearn",
        "pyyaml",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            "phishing-detection=phishing_detection.cli:main",
        ],
    },
)
