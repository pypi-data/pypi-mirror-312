============
Contribution
============

Contributions are highly welcomed and appreciated.

.. contents::
   :depth: 2
   :backlinks: none

Feature requests
----------------

We'd also like to hear about your thoughts and suggestions.  Feel free to
`submit them as issues <https://github.com/reportportal/client-Python/issues>`_ and:

* Explain in detail how they should work.
* Keep the scope as narrow as possible. It will make it easier to implement.

Bug reports
-----------

Report bugs for the client in the `issue tracker <https://github.com/reportportal/client-Python/issues>`_.

If you are reporting a new bug, please include:

* Your operating system name and version.
* Python interpreter version, installed libraries, and reportportal-client
  version.
* Detailed steps to reproduce the bug.

Bug fixes
---------

Look through the `GitHub issues for bugs <https://github.com/reportportal/client-Python/labels/bug>`_.

If you are gonna fix any of existing bugs, assign that bug to yourself and specify preliminary milestones.
Talk to `contributors <https://github.com/reportportal/client-Python/graphs/contributors>`_ in case you need a
consultancy regarding implementation.

Implement features
------------------

Look through the `GitHub issues for enhancements <https://github.com/reportportal/client-Python/labels/enhancement>`_.

Talk to `contributors <https://github.com/reportportal/client-Python/graphs/contributors>`_ in case you need a
consultancy regarding implementation.

Preparing Pull Requests
-----------------------

What is a "pull request"?  It informs the project's core developers about the
changes you want to review and merge.  Pull requests are stored on
`GitHub servers <https://github.com/reportportal/client-Python/pulls>`_.
Once you send a pull request, we can discuss its potential modifications and
even add more commits to it later on. There's an excellent tutorial on how Pull
Requests work in the
`GitHub Help Center <https://help.github.com/articles/using-pull-requests/>`_.

Here is a simple overview below:

#. Fork the
   `reportportal-client GitHub repository <https://github.com/reportportal/client-Python>`_.

#. Clone your fork locally using `git <https://git-scm.com/>`_ and create a branch::

    $ git clone git@github.com:YOUR_GITHUB_USERNAME/client-Python.git
    $ cd client-Python
    # now, create your own branch off the "master":

        $ git checkout -b your-bugfix-branch-name

   If you need some help with Git, follow this quick start
   guide: https://git.wiki.kernel.org/index.php/QuickStart

#. Install `pre-commit <https://pre-commit.com>`_ and its hook on the client-Python repo:

   **Note: pre-commit must be installed as admin, as it will not function otherwise**::

     $ pip install --user pre-commit
     $ pre-commit install

   Afterwards ``pre-commit`` will run whenever you commit.

   https://pre-commit.com/ is a framework for managing and maintaining multi-language pre-commit hooks
   to ensure code-style and code formatting is consistent.

#. Install tox

   Tox is used to run all the tests and will automatically setup virtualenvs
   to run the tests in.
   (will implicitly use http://www.virtualenv.org/en/latest/)::

    $ pip install tox

#. Run all the tests

   You need to have Python 3.6 available in your system.  Now
   running tests is as simple as issuing this command::

    $ tox -e pep,py36

   This command will run tests via the "tox" tool against Python 3.6
   and also perform code style checks.

#. You can now edit your local working copy and run the tests again as necessary. Please follow PEP-8 recommendations.

   You can pass different options to ``tox``. For example, to run tests on Python 3.6 and pass options to pytest
   (e.g. enter pdb on failure) to pytest you can do::

    $ tox -e py36 -- --pdb

   Or to only run tests in a particular test module on Python 3.6::

    $ tox -e py36 -- tests/test_service.py


   When committing, ``pre-commit`` will re-format the files if necessary.

#. If instead of using ``tox`` you prefer to run the tests directly, then we suggest to create a virtual environment and use
   an editable install with the ``testing`` extra::

       $ python3 -m venv .venv
       $ source .venv/bin/activate  # Linux
       $ .venv/Scripts/activate.bat  # Windows
       $ pip install -e ".[testing]"

   Afterwards, you can edit the files and run pytest normally::

       $ pytest tests/test_service.py


#. Commit and push once your tests pass and you are happy with your change(s)::

    $ git commit -m "<commit message>"
    $ git push -u


#. Finally, submit a pull request through the GitHub website using this data::

    head-fork: YOUR_GITHUB_USERNAME/client-Python
    compare: your-branch-name

    base-fork: reportportal/client-Python
    base: master
