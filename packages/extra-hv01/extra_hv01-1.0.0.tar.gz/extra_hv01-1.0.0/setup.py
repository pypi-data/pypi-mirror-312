from setuptools import setup, find_packages

setup(
    name     = "extra-hv01",
    version  = "1.0.0",
    description = "A sample packages with hierarchical modules",
    author   = "Harold Vasquez",
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False
)
