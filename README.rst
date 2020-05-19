=============================
Structurizr for Python
=============================

.. image:: https://img.shields.io/pypi/v/structurizr-python.svg
   :target: https://pypi.org/project/structurizr-python/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/structurizr-python.svg
   :target: https://pypi.org/project/structurizr-python/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/structurizr-python.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: https://github.com/Midnighter/structurizr-python/blob/master/.github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://codecov.io/gh/Midnighter/structurizr-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/structurizr-python
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

.. image:: https://readthedocs.org/projects/structurizr-python/badge/?version=latest
   :target: https://structurizr-python.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. summary-start

A Python client package for the Structurizr cloud service and on-premises installation.

Post Template-Instantiation Steps
=================================

1. Start working with git.

   .. code-block:: console

       git init

2. Check for an updated versioneer.

   .. code-block:: console

       pip install versioneer
       versioneer install

   You probably have to remove the mess in ``src/structurizr/__init__.py``.

3. Commit all the files.

   .. code-block:: console

       git add .
       git commit

4. Create a repository on `GitHub <https://github.com/>`_ if you haven't done
   so yet and link it to `Travis CI <https://travis-ci.org/>`_.
5. Browse through the architecture decision records (``docs/adr``) if you want
   to understand details of the package design.
6. Remove this section from the readme and describe what your package is all
   about.
7. When you're ready to make a release, perform the following steps.

   1. On `Travis CI <https://travis-ci.org/>`_ set the secure environment
      variables ``PYPI_USERNAME``, ``PYPI_PASSWORD``, and ``GITHUB_TOKEN``.
   2. Tag your latest commit with the desired version and let Travis handle
      the release.

      .. code-block:: console

          git tag 0.1.0
          git push origin 0.1.0

Install
=======

It's as simple as:

.. code-block:: console

    pip install structurizr-python

Copyright
=========

* Copyright © 2020, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. summary-end
