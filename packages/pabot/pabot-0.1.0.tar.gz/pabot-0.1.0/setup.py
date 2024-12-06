from setuptools import setup, find_packages

setup(
    name="pabot",
    version="0.1.0",
    description="Redirect package for robotframework-pabot",
    author="Mikko Korpela",
    author_email="mikko.korpela@gmail.com",
    url="https://github.com/mkorpela/pabot",
    packages=find_packages(),
    install_requires=[
        "robotframework-pabot",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
