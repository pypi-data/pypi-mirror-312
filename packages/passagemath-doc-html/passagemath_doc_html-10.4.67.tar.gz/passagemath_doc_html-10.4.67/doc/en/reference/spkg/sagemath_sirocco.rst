.. _spkg_sagemath_sirocco:

============================================================================================
sagemath_sirocco: Certified root continuation with sirocco
============================================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2024 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (Windows Subsystem for Linux).

See https://doc.sagemath.org/html/en/installation/index.html
for general installation instructions.


About this pip-installable source distribution
----------------------------------------------

This pip-installable source distribution ``sagemath-sirocco`` is a small
optional distribution for use with ``sagemath-standard``.

It provides a Cython interface to the ``sirocco`` library for the purpose
of compute topologically certified root continuation of bivariate polynomials.

Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cypari`
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_mpfr`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_environment`
- :ref:`spkg_sirocco`

Version Information
-------------------

package-version.txt::

    10.4.67

version_requirements.txt::

    passagemath-sirocco ~= 10.4.67.0


Equivalent System Packages
--------------------------

.. tab:: conda-forge

   .. CODE-BLOCK:: bash

       $ conda install sagemath-sirocco 



However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.

