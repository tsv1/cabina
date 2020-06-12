from setuptools import find_packages, setup


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()


setup(
    name="cabina",
    version="0.0.1",
    description="Configuration without magic",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="nikitanovosibirsk@yandex.com",
    python_requires=">=3.6.0",
    url="https://github.com/nikitanovosibirsk/cabina",
    license="Apache-2.0",
    packages=find_packages(exclude=("tests",)),
    install_requires=find_required(),
    tests_require=find_dev_required(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
)
