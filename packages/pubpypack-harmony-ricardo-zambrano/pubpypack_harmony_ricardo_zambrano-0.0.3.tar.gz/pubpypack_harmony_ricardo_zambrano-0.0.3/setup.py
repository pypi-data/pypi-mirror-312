from setuptools import setup
from Cython.Build import cythonize

PATH = "./src/imppkg/harmonic_mean.pyx"

setup (
    ext_modules = cythonize(PATH),
)
