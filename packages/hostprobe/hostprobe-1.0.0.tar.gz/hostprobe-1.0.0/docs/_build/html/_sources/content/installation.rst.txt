:orphan:

Downloading and Installing hostprobe
===============================================

Downloading Python + pip
-------------------------------

To install hostprobe, make sure you have python 3.7+, and pip installed.
To install the latest python version, go to https://www.python.org/downloads/ and install 
the latest version of python (or any version greater than 3.7).

To check if pip was installed with python, try
``pip --version``. If pip was not installed, use

.. code-block:: bash

    python -m ensurepip --upgrade

to install pip, or verify the integrity of your pip installation

Normal hostprobe installation
-------------------------------------------

The best way of installing hostprobe is through pip:

.. code-block:: bash

    pip install hostprobe


Github install through pip
-------------------------------

If you wish to install hostprobe version from github (good for getting prereleases), use:

.. code-block:: bash

    pip install hostprobe@git+https://github.com/malachi196/hostprobe


ARM64
-------------------------------

If you are using an ARM64 device (such as raspberry pi), you may need to use

.. code-block:: bash

    pip install hostprobe --break-system-packages

if you want to install the package ouside of a venv (Virtual ENVironment)
