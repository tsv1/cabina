from setuptools import find_packages, setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()


setup(
    name="cabina",
    version="1.1.0",
    description="Configuration with typed env vars",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="tsv1@fastmail.com",
    python_requires=">=3.8",
    url="https://github.com/tsv1/cabina",
    license="Apache-2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"cabina": ["py.typed"]},
    install_requires=find_required(),
    tests_require=find_dev_required(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Typing :: Typed",
    ],
)
