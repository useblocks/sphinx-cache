Nitpicker CI Docs
=================

Nitpicker CI is a flexible CLI tool for QA which checks certain requirements before and after CI builds.

For Toolchain qualification, you need a tool to check certain requirements before and after CI builds. For instance it shall check, if Sphinx was run in incremental build or not.

By nature, these kinds of checks are quite numerous and differ a lot (checking logs, return values, HW requirements, …).

With Nitpicker CI, we handle the **checks** like normal **test cases** for software, so they are just a single check-function in a check-file.

As Nitpicker CI behaves like a test-framework, we use the **pytest** test-framework to execute all our checks.
So pytest is collecting and executing all our checks, and summarizing the results.

Overview
--------

1. Install the Nitpicker CI tool by running the following command:
    .. code-block:: bash

        $ pip install nitpicker-ci
2. After installing the tool, you can use it in your command line terminal. You can verify if the installation was successful by checking the version of the tool:
    .. code-block:: bash

        $ nitpicker-ci --version  # Outputs: Nitpicker CI, version 0.0.1

3. Create a new **check-directory** with any name of your choice (e.g. *ci_checks*) and store an **__init__.py** file in it.
4. Inside the new check-directory, you can create multiple **check-file(s)** (e.g. *ci_checks_\*.py*) and write your own **check-function(s)** in it. Below is an example of a check-function:
    .. code-block:: python

        import pytest

        def check_function():
            a = 10
            assert a % 2 == 0
5. Run the Nitpicker CI tool to examine if the **checks** are successful or not by using the ``check`` command with its options. The example below uses *ci_checks* as **check-directory**, *ci_checks_\*.py* as **check-file**, and uses the default prefix (*check*) to identify **check-functions**.
    .. code-block:: bash

        $ nitpicker_ci check --test-dir ci_checks --file-prefix ci_checks_*.py

        ============================= test session starts ==============================
        platform linux -- Python 3.9.5, pytest-7.3.0, pluggy-1.0.0
        rootdir: /home/user/nitpicker
        configfile: pyproject.toml
        testpaths: ci_checks
        collected 1 items

        ci_checks/ci_checks_basic_doc.py ..                                              [1/1]

        ============================== 1 passed in 0.001s ===============================
        [nitpicker] ✅ OK

.. note::

    For more information about the CLI tool, please run the :bash:`nitpicker --help` command in your terminal.

We have created the Sphinx-Cache library.



.. toctree::
   :maxdepth: 1
   :hidden:

    test