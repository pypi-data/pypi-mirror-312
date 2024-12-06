.. _The Inspect Command:

The Inspect Command
===================

The ``inspect`` command allow to investigate more deeply
on a specific contributor profile that have been potentially
considered as suspicious by the ``analyze`` command (
:ref:`The Analyze Command`).

.. code-block::

    $ defected inspect [OPTIONS]


You can list all the available options by using:

.. code-block::

    $ defected inspect -h

Examples of Usage
-----------------

To inspect a specific contributor on a remote repository by
providing its URL and by specifing either the name, the email,
or both data about the contributor that you want to investigate:

.. code-block::

    $ defected inspect \
        --repo https://github.com/user/repo.git \
        --user "John Doe"

If you want to ease your investigation you can filter only on
suspicious results by using ``--only-suspicious`` flag. The
following command display and export only the activity of the
contributors named John Doe and flagged as suspicious:

.. code-block::

    $ defected inspect \
        --repo https://github.com/user/repo.git \
        --user "John Doe"
        --only-suspicious

Examples Output
---------------

Here is an example of terminal output:

.. code-block::

    $ defected inspect \
        --repo https://github.com/user/repo.git \
        --user "John Doe"
        --only-suspicious
    Commits found for John Doe: 43

    Timezone usage:
      timezone  commit_count
    0    +0800            37
    1    +0300             3
    2    +0200             3

    Timezone change log:
    From +0800 at 2024-10-06 17:00:38 to +0300 at 2024-10-06 21:53:09 (SUSPICIOUS)
    From +0300 at 2024-06-27 17:27:09 to +0800 at 2024-06-27 23:38:32 (SUSPICIOUS)
    From +0200 at 2024-02-12 17:09:10 to +0800 at 2024-02-13 01:53:33 (SUSPICIOUS)

If you want to go further in your investigation you can take
a look to our cold cases to see the patterns revealed in real
attacks:

.. toctree::
   :maxdepth: 1
   :glob:

   examples/investigations/*
