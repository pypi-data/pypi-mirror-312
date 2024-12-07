"""Setup module for nettigo_air_monitor."""

from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "4.0.0"

setup(
    name="nettigo_air_monitor",
    version=VERSION,
    author="Maciej Bieniek",
    description=(
        "Python wrapper for getting air quality data from Nettigo Air Monitor devices."
    ),
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/bieniu/nettigo-air-monitor",
    license="Apache-2.0",
    packages=["nettigo_air_monitor"],
    package_data={"nettigo_air_monitor": ["py.typed"]},
    python_requires=">=3.12",
    install_requires=["aiohttp>=3.9.4", "aqipy-atmotech", "dacite>=1.7.0", "tenacity"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
)
