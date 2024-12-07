# controlib

A Python package for control system design and deployment.

ControLib is a package to help users design advanced control systems, test and benchmark them, and deploy them on a few selected embedded platforms (Arduino, STM32 Nucleo, Raspberry Pi). By advanced, we are referring to control systems beyond the realm of classical control (e.g. Model Predictive Control), especially those that are heavily reliant on machine learning and/or optimisation. Some classical control systems (e.g. PID controllers) will be included as well.

Some Simulink models will also be provided. To interact with these using Python, ControLib will use the [PySimlink](https://github.com/lharri73/PySimlink) package.

ControLib will support Software-in-the-loop, Processor-in-the-loop, and Hardware-in-the-loop testing, although the extent to which it will do so is yet to be determined.

Please note that development is still in the very early stages, and it might take a while before a stable version is released.

# Features

The package's main features and capabilities will be announced and listed here as soon as they are added.

# Installation

## Using pip

The package can be installed via pip:

```
pip install controlib
```

## Using git

Alternatively, you can download the package directly from Github. To do so, clone the repository:

```
git clone https://github.com/MiguelLoureiro98/controlib.git
```

Then, move into the package's directory and install it using pip:

```
cd controlib
pip install .
```

# Documentation

An official documentation website containing installation instructions, user guides, an API reference, examples, and a contribution guide,  will be released soon.

# Known Issues

Nothing to report.

# Licence

This package is licenced under the [GNU General Public License v3.0](LICENSE).

# About

ControLib is currently being developed and maintained by Miguel Loureiro, a mechanical engineer who specialises in control systems, machine learning, and optimisation.
