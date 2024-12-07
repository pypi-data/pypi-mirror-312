from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ds_sale_prediction_package",
    version="0.1.3",
    description="A package for data preparation, feature extraction\
    model training, and making prediction",
    author="Aliona Hrynkevich",
    packages=find_packages(),
    install_requires=requirements,
)
