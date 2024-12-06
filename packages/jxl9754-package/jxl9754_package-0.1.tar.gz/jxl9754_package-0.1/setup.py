from setuptools import setup

setup(
    name="jxl9754_package",
    version="0.1",
    description="A sample Python package",
    author="John Doe",
    author_email="jdoe@example.com",
    packages=["jxl9754_package"],
    install_requires=[
        "numpy",
        "pandas",
    ],
)


# python3 setup.py sdist bdist_wheel
