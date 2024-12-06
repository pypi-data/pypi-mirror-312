.. _The Analyze Command:

The Analyze Command
===================

The `analyze` command give you a quick overview of
contributors profiles that can be potentially considered
as suspicious.

.. code-block::

    $ defected analyze [OPTIONS]


You can list all the available options by using:

.. code-block::

    $ defected analyze -h

Examples of Usage
-----------------

To analyze timezone changes on local git repository for:

.. code-block::

    $ defected analyze


You are also able to analyze a remote repository.
The following command analyze a remote repository by providing its URL:

.. code-block::

    $ defected analyze --repo https://github.com/user/repo.git

If you want to ease your investigation you can filter only on
suspicious results. The follow command display and export only
contributors flagged as suspicious:

.. code-block::

    $ defected analyze --only-suspicious
    $ # or
    $ defected analyze \
        --repo https://github.com/user/repo.git \
        --only-suspicious

Examples Output
---------------

Here is an example of terminal output:

.. code-block::

    Extracting Git logs...
    150 commits extracted.

    Analyzing timezones with a threshold of 2 timezone changes...

    Showing only suspicious results:
                author             email      total_commits  unique_timezones  timezone_changes  suspicious
    0    Alice Smith    alice@example.com     45              3                4                True
    1    Bob Johnson    bob@example.com       30              2                3                True

    Saving analysis to 'timezone_analysis.csv'...
    Analysis saved.

Or CSV output:

.. list-table:: timezone_analysis.csv
   :header-rows: 1

   * - author
     - total_commits
     - unique_timezones
     - timezone_changes
     - suspicious
     - email
   * - Alice Smith
     - 45
     - 3
     - 4
     - True
     - alice@example.com
   * - Bob Johnson
     - 30
     - 2
     - 3
     - True
     - bob@example.com

If you want to go further in your investigation
we invite you take a look at the :ref:`The Inspect Command`.
