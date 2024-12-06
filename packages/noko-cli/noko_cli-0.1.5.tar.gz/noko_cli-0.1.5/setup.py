import os
import logging

from setuptools import find_packages, setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup(
    name="noko_cli",
    version="0.1.5",
    description="A simple CLI interface for Noko time tracking.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "python-freckle-client",
        "python-dotenv",
    ],
    entry_points="""
        [console_scripts]
        noko_cli_setup=source.setup.setup:setup
        ncs=source.setup.setup:setup
        noko_log=source.noko_logger.time_logger:log
        nl=source.noko_logger.time_logger:log
    """,
)
