import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup


module_name = "tldl"
module = SourceFileLoader(
    module_name, os.path.join(module_name, "__init__.py")
).load_module()


def load_requirements(fname: str) -> list:
    requirements = []
    with open(fname, "r") as fp:
        for req in parse_requirements(fp.read()):
            extras = "[{}]".format(",".join(req.extras)) if req.extras else ""
            requirements.append("{}{}{}".format(req.name, extras, req.specifier))
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    description=module.__doc__,
    url="https://github.com/itmo-dev-days-2024/tldl",
    platforms="all",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: Russian",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
    ],
    python_requires=">=3.12",
    packages=find_packages(exclude=["tests"]),
    install_requires=load_requirements("requirements.txt"),
    extras_require={"dev": load_requirements("requirements.dev.txt")},
    entry_points={
        "console_scripts": [
            "{0}-bot = {0}.main:main".format(module_name),
            "{0}-db = {0}.db:main".format(module_name),
            "{0}-worker = {0}.jobs.worker:_main".format(module_name),
        ]
    },
    include_package_data=True,
)
