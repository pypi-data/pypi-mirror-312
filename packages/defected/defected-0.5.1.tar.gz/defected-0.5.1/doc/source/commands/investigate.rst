.. _The Investigate Command:

The Investigate Command
=======================

The goal of the ``investigate`` command is to investigate
suspicious timezone changes that have been found
by the ``inspect`` command (:ref:`The Inspect Command`), and
to provide transposed times, countries, and travel feasibility.

You can list all the available options by using:

.. code-block::

    $ defected inspect -h

Examples of Usage
-----------------

The ``investigate`` command allow you to configure
travel speed, by default set a average flight speed (900km/h).
This way you are able to check if the timezone change is credible
(physically possible) or not.

.. code-block::

    $ defected investiage \
        --file output-from-inspect.csv

This command work from the results obtained by using the
``inspect`` command and it give you informations like
time comparions, physical location behind timezone, etc.

This command give more meaning to data.

Examples Output
---------------

Here is an example of terminal output:

.. code-block::

    $ defected investiage \
        --file output-from-inspect.csv
    Investigation results saved to 'investigate_results.csv'.
         date_of_change previous_timezone                                              countries_previous current_timezone                                               countries_current                                                        departure                                                          arrival  physically_possible
    2022-10-06 17:00:38             +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore            +0300     Asia, Antarctica, Etc, Europe, Indian, W-SU, Turkey, Africa 2022-10-06 17:00:38 +0800 (estimated time at arrival: 2022-10-06 12:00:38 +0300) 2022-10-06 21:53:09 +0300 (estimated time at departure: 2022-10-07 02:53:09 +0800)                 True
    2023-06-27 17:27:09             +0300     Asia, Antarctica, Etc, Europe, Indian, W-SU, Turkey, Africa            +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore 2023-06-27 17:27:09 +0300 (estimated time at arrival: 2023-06-27 22:27:09 +0800) 2023-06-27 23:38:32 +0800 (estimated time at departure: 2023-06-27 18:38:32 +0300)                False
    2024-02-12 17:09:10             +0200            Asia, Libya, EET, Etc, Israel, Europe, Africa, Egypt            +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore 2024-02-12 17:09:10 +0200 (estimated time at arrival: 2024-02-12 23:09:10 +0800) 2024-02-13 01:53:33 +0800 (estimated time at departure: 2024-02-12 19:53:33 +0200)                False


.. list-table:: Generated report
   :header-rows: 1

   * - date_of_change
     - previous_timezone
     - countries_previous
     - current_timezone
     - countries_current
     - departure
     - arrival
     - physically_possible
   * - 2022-10-06 17:00:38
     - +0800
     - Asia, Hongkong, Singapore, Antarctica, Australia, ROC, PRC, Etc
     - +0300
     - Europe, Turkey, Asia, Africa, Antarctica, Indian, W-SU, Etc
     - 2022-10-06 17:00:38 +0800 (estimated time at arrival: 2022-10-06 12:00:38 +0300)
     - 2022-10-06 21:53:09 +0300 (estimated time at departure: 2022-10-07 02:53:09 +0800)
     - True
   * - 2023-06-27 17:27:09
     - +0300
     - Europe, Turkey, Asia, Africa, Antarctica, Indian, W-SU, Etc
     - +0800
     - Asia, Hongkong, Singapore, Antarctica, Australia, ROC, PRC, Etc
     - 2023-06-27 17:27:09 +0300 (estimated time at arrival: 2023-06-27 22:27:09 +0800)
     - 2023-06-27 23:38:32 +0800 (estimated time at departure: 2023-06-27 18:38:32 +0300)
     - False
   * - 2024-02-12 17:09:10
     - +0200
     - EET, Europe, Asia, Libya, Israel, Africa, Egypt, Etc
     - +0800
     - Asia, Hongkong, Singapore, Antarctica, Australia, ROC, PRC, Etc
     - 2024-02-12 17:09:10 +0200 (estimated time at arrival: 2024-02-12 23:09:10 +0800)
     - 2024-02-13 01:53:33 +0800 (estimated time at departure: 2024-02-12 19:53:33 +0200)
     - False

.. include:: ../cold-case-banner.rst
