from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import pybind11
import subprocess

# Lesen der README-Datei (optional)
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "KIB package description."

# Definiere die Erweiterung für pybind11
ext_modules = [
    Extension(
        "KIB_LAP.plate_buckling_cpp",  # Modulname (muss mit dem Python-Import übereinstimmen)
        ["KIB_LAP/Plattenbeulen/plate_buckling.cpp"],  # Pfad zur C++-Datei
        include_dirs=[
            pybind11.get_include(),  # Include-Verzeichnis von pybind11
        ],
        language="c++"  # Sprache ist C++
        ),
        Extension(
        "KIB_LAP.plate_bending_cpp",  # Modulname (muss mit dem Python-Import übereinstimmen)
        ["KIB_LAP/Plattentragwerke/plate_bending.cpp",
         "KIB_LAP/Plattentragwerke/Functions.cpp",
        'KIB_LAP/Plattentragwerke/NumericalIntegration.cpp'],  # Pfad zur C++-Datei
        include_dirs=[
            pybind11.get_include(),  # Include-Verzeichnis von pybind11
            pybind11.get_include(True),
            '.',  # Fügen Sie das aktuelle Verzeichnis hinzu
        ],
        language="c++"  # Sprache ist C++
    )
]

# Konfiguration der Bibliothek
setup(
    name="KIB_LAP",
    version="0.2.5.1.6",
    packages=find_packages(),
    include_package_data=True,
    description="A package for structural engineering calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="leoth",
    author_email="thomas.leonard@outlook.de",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pybind11>=2.6"  # pybind11 als Abhängigkeit hinzufügen
    ],
    ext_modules=ext_modules,  # Erweiterungen (C++-Module) hinzufügen
    cmdclass={"build_ext": build_ext},  # Build-Kommando für Erweiterungen
)
