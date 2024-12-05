from setuptools import setup, find_packages

setup(
    name="revealcontrol",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["check_cf_association"],
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "revealcontrol=check_cf_association:main",
        ],
    },
)