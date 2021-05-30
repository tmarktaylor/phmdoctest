"""A setuptools based setup module.
"""

# See setup.cfg.
# Note:
# Entry points done here since setuptools minimum version
# for this section in setup.cfg is 51.0.0 per
# https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
# Always prefer setuptools over distutils
from setuptools import setup

setup(
    entry_points={
        "console_scripts": [
            "phmdoctest=phmdoctest.main:entry_point",
        ],
    },
)
