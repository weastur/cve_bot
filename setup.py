import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = "cve_bot"

module = SourceFileLoader(
    module_name, os.path.join(module_name, "__init__.py")
).load_module()


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, "r") as fp:
        for req in parse_requirements(fp.read()):
            extras = "[{0}]".format(",".join(req.extras)) if req.extras else ""
            requirements.append(
                "{0}{1}{2}".format(req.name, extras, req.specifier)
            )
    return requirements


with open("README.md") as readme:
    long_description = readme.read()

setup(
    name=module.__name__,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weastur/cve_bot",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: System",
        "Topic :: System :: Operating System",
        "Topic :: System :: Systems Administration",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=load_requirements("requirements.txt"),
    extras_require={"dev": load_requirements("requirements.dev.txt")},
    entry_points={
        "console_scripts": [
            "{0} = {0}.main:main".format(module_name),
        ]
    },
    package_data={
        "cve_bot": ["alembic.ini", "migrations/versions/*.py"],
    },
)
