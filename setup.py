from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info("setup.py entered")
log.info("$PATH=%s" % os.environ["PATH"])

name = "idom_jupyter"
LONG_DESCRIPTION = "A client for IDOM implemented using Jupyter widgets"

# Get idom_jupyter version
version = get_version(pjoin(name, "_version.py"))

js_dir = pjoin(here, "js")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(js_dir, "dist", "index.js"),
]

data_files_spec = [
    (
        "share/jupyter/nbextensions/idom-client-jupyter",
        "idom_jupyter/nbextension",
        "*.*",
    ),
    (
        "share/jupyter/labextensions/idom-client-jupyter",
        "idom_jupyter/labextension",
        "**",
    ),
    (
        "share/jupyter/labextensions/idom-client-jupyter",
        ".",
        "install.json",
    ),
    (
        "etc/jupyter",
        "jupyter-config",
        "**/*.json",
    ),
]

cmdclass = create_cmdclass("jsdeps", data_files_spec=data_files_spec)
cmdclass["jsdeps"] = combine_commands(
    install_npm(js_dir, npm=["yarn"], build_cmd="build:prod"),
    ensure_targets(jstargets),
)

setup_args = dict(
    name=name,
    version=version,
    description="A client for IDOM implemented using Jupyter widgets",
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    install_requires=["ipywidgets>=7.6.0", "idom>=0.23.0,<0.24.0"],
    packages=find_packages(),
    zip_safe=False,
    cmdclass=cmdclass,
    author="Ryan Morshead",
    author_email="ryan.morshead@gmail.com",
    url="https://github.com/idom-team/idom-jupyter",
    keywords=[
        "ipython",
        "jupyter",
        "widgets",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: IPython",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

setup(**setup_args)
