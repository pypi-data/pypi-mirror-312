#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command, find_namespace_packages

# Package meta-data.
NAME = "phenotools"
DESCRIPTION = "A user-friendly tool for breeders to extract organ-level phenotypic traits from UAV imagery."
URL = "https://phenonet.org/phenosr"
EMAIL = "ruinan@stu.njau.edu.cn"
AUTHOR = "Ruinan Zhang"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = "0.1.2"

# What packages are required for this module to be executed?
REQUIRED = [
    "dj-rest-auth==6.0.0",
    "Django==4.2.7",
    "django-allauth==64.0.0",
    "django-comment-migrate==0.1.7",
    "django-cors-headers==4.3.0",
    "django-filter==23.3",
    "django-huey==1.2.0",
    "django-ranged-response==0.2.0",
    "django-redis==5.4.0",
    "django-rest-swagger==2.2.0",
    "django-restql==0.15.3",
    "django-simple-captcha==0.5.20",
    "django-timezone-field==6.0.1",
    "djangorestframework==3.14.0",
    "djangorestframework-jwt==1.11.0",
    "djangorestframework-simplejwt==5.3.0",
    "einops==0.8.0",
    "huey==2.5.1",
    "imageio==2.35.1",
    "kombu==5.3.7",
    "loguru==0.7.2",
    "matplotlib==3.9.2",
    "netifaces==0.11.0",
    "numpy==1.26.4",
    "opencv-python==4.10.0.84",
    "pillow==10.4.0",
    "PyJWT==1.7.1",
    "pynvml==11.5.0",
    "pytorch-msssim==1.0.0",
    "psutil==6.0.0",
    "PyYAML==6.0.1",
    "scikit-image==0.24.0",
    "scipy==1.13.1",
    "seaborn==0.13.2",
    "SQLAlchemy==2.0.30",
    "torch==1.11.0",
    "torchvision==0.12.0",
    "basicsr>=1.4.2",
    "drf_yasg==1.21.7",
    "tqdm==4.66.4",
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_namespace_packages(),
    include_package_data=True,
    package_data={
        "backend": [
            "add.sqlite3",
            "db.sqlite3",
            "config.ini",
            "version.json",
            "queue.sqlite3",
            "logs/*",
            "logs/web/system.log",
            "task/config/sr/finetune_5d4780bd-7965-7e89-0ad8-7e2205aeecc4.yaml",
            "task/config/sr/train_5d4780bd-7965-7e89-0ad8-7e2205aeecc4.yaml",
            "task/config/sr/train_sr.yaml",
        ]
    },
    entry_points={
        "console_scripts": [
            "phenotools-w=phenotools.__main__:main",
            "phenotools-q=phenotools.__main__:djangohuey",
        ],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license="GPL3.0",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
