from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = "karolis_s_mod1_atsiskaitymas",
    packages = find_packages(),
    version = "1.0.1",
    author = "Karolis",
    author_email = "karolis.skruibis@codeacademylt.onmicrosoft.com",
    install_requires = [
        #install requests
        #install lxml
        #install csv
        #install twine
        #install setuptools
        #install wheel
    ],
    entry_points = {"console_scripts": ["karolis_crawl=karolis_s_mod1_atsiskaitymas.main:crawl_gintarine"]},
    long_description = description,
    long_description_content_type="text/markdown",
)