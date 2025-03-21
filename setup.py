import os
import shutil
import re
import sys

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop
from distutils.command.clean import clean as _clean


def paramsets():
    pattern = "params-sphincs-([a-zA-Z-][a-zA-Z0-9-]*).h"
    pfiles = os.listdir(os.path.join("src", "sphincsplus", "ref", "params"))
    for paramset in pfiles:
        try:
            yield re.search(pattern, paramset).group(1).replace('-', '_')
        except AttributeError:
            raise Exception("Cannot parse name of parameter set {}"
                            .format(paramset))


def create_param_wrappers():
    for paramset in paramsets():
        with open(os.path.join("src", "pyspx_slhdsa", paramset + ".py"), 'w') as f:
            f.write(
                "from pyspx_slhdsa.bindings import PySPXBindings as _PySPXBindings\n"
                "from pyspx_slhdsa.tests import PySPXTests as _PySPXTests\n"
                "from _spx_{} import ffi as _ffi, lib as _lib\n"
                "\n"
                "import sys\n"
                "\n"
                "sys.modules[__name__] = _PySPXTests().test_paramset(_PySPXBindings(_ffi, _lib), '{}')\n"
                .format(paramset, paramset)
            )


class build_py(_build_py):

    def run(self):
        create_param_wrappers()
        _build_py.run(self)


class develop(_develop):

    def run(self):
        create_param_wrappers()
        _develop.run(self)


class clean(_clean):

    def run(self):
        for paramset in paramsets():
            try:
                os.remove(os.path.join("src", "pyspx_slhdsa", paramset + ".py"))
            except:
                pass
            if sys.version_info[0] < 3:
                objname = "_spx_{}.so".format(paramset)
            else:
                objname = "_spx_{}.abi3.so".format(paramset)
            try:
                os.remove(os.path.join("src", objname))
            except:
                pass
        shutil.rmtree(os.path.join("src", "sphincsplus-instances"))
        _clean.run(self)


with open('README.md') as f:
    long_description = f.read()

setup(
    name="PySPX_SLHDSA",
    version="0.5.1",
    packages=['pyspx_slhdsa'],
    author="Joost Rijneveld, Peter Schwabe, Ruben Gonzalez",
    author_email='contact@sphincs.org',
    url="https://github.com/tmcqueen-materials/pyspx-slhdsa",
    description='Python bindings for SPHINCS+ with SLH-DSA parameters',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    classifiers=[
        'Topic :: Security :: Cryptography',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
    ],
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    tests_require=["pytest", "cffi>=1.0.0"],
    cffi_modules=["src/pyspx_slhdsa/build.py:{}".format(x) for x in paramsets()],
    cmdclass={
        "build_py": build_py,
        "develop": develop,
        "clean": clean,
    },
    zip_safe=False,
)
