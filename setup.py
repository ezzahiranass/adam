from setuptools import setup, find_packages

setup(
    name="adam",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "cadquery",
        "shapely",
        "ifcopenshell",
        "numpy",
        "scipy",
        # Add other dependencies here
    ],
    author="Your Name",
    description="Parametric modeling framework for architectural research",
)
