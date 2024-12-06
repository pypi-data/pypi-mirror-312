.. _The XZ Utils backdoor:

The XZ Utils backdoor
=====================

.. warning::
    **Before starting investigating this cold case, we should notice that
    it is now easy to understand the whole story after the fact. We do not
    want to be perceived as patronizing or as moralizers. In no case we
    want to incriminate anyone. We simply want to highligh
    such kind of social engineering to try to limit as far as possible
    similar scenarios in the future.**

    Lasse Collin and Jonathan Nieder are persons mentioned in this example
    but they are not any time responsible of anything or badly intentioned.
    They are just mentioned in this example because their name bubbled
    up at the beginning of the investigation due to some false alarm,

    The scope of this investigation only focus on **Jia Tan** who
    have been proven as badly intentioned.

    We didn't investigated further about other results and so we
    consider them as false alarm.

In this example we describe the story of `JiaT75
<https://github.com/JiaT75>`_ (Jia Tan), a core contributor of the
`xz utils project <https://github.com/tukaani-project/xz/>`_,
`who introduced a backdoor into that deliverable
<https://en.wikipedia.org/wiki/XZ_Utils_backdoor>`_.

Background
----------

In February 2024, a contributor named `JiaT75
<https://github.com/JiaT75>`_ managed to introduce a backdoor into
the popular compression utility **xz**. This backdoor could have
allowed unauthorized access to systems using the library, creating a
serious security risk.

Upon investigation, it was discovered that **JiaT75** exhibited
**suspicious behavior**:

1. He made commits from multiple, rapidly-changing timezones over
   a short period.
2. His activity patterns were inconsistent with typical open source
   contributors, suggesting potential misuse of accounts or automation.

Defected can help identify such patterns in contributors' Git activity.

Detecting JiaT75's Behavior with Defected
-----------------------------------------

Suppose you are a maintainer of the **xz** project and you suspect
malicious activity. You can use the ``defected`` command to analyze
the commit logs for anomalies.

Let's analyze the xz repository:

.. code-block::

   $ pip install defected
   $ defected analyze \
       --repo https://github.com/tukaani-project/xz \
       --only-suspicious

This command will output something like the following:

.. code-block::

   Cloning remote repository: https://github.com/tukaani-project/xz...
   Extracting Git logs...
   2676 commits extracted.
   Parsing logs...
   Analyzing timezones with a threshold of 2 timezone changes...

   Showing only suspicious results:
                author  total_commits  unique_timezones  timezone_changes  suspicious                     email
   36     Lasse Collin           2102                 3                36        True  lasse.collin@tukaani.org
   28          Jia Tan            449                 3                14        True        jiat0218@gmail.com
   32  Jonathan Nieder              9                 3                 4        True        jrnieder@gmail.com

   Saving analysis to 'timezone_analysis.csv'...
   Analysis saved.

Results are exported at the CSV format and can be loaded in sheet:

.. list-table:: timezone_analysis.csv
   :header-rows: 1

   * - author
     - total_commits
     - unique_timezones
     - timezone_changes
     - suspicious
     - email
   * - Lasse Collin
     - 2102
     - 3
     - 36
     - True
     - lasse.collin@tukaani.org
   * - Jia Tan
     - 449
     - 3
     - 14
     - True
     - jiat0218@gmail.com
   * - Jonathan Nieder
     - 9
     - 3
     - 4
     - True
     - jrnieder@gmail.com

The ``analyze`` command identified 3 contributors profils that
are potentially suspicious due to timezone changes.

.. note::
   The `analyze` command can raise false alarm. The usage of the
   `inspect` command and a manual investigation on the results
   of the `analyze` command is required to incriminate or discriminate
   a suspicious activity.

At this point the previous command is not enough to determine if
these persons are badly intentioned or not.

The next step of our investigation is to use the ``inspect`` command.

Lets focus on the Jia Tan profile. We can found more useful details
about Jia Tan by running the following command:

.. code-block::

    $ defected inspect \
        --repo https://github.com/tukaani-project/xz \
        --user "Jia Tan"
    Commits found for Jia Tan: 450

    Timezone usage:
      timezone  commit_count
    0    +0800           441
    1    +0300             6
    2    +0200             3

    Timezone change log:
    From +0800 at 2022-06-13 20:27:03 to +0300 at 2022-06-16 17:32:19
    From +0300 at 2022-06-16 17:32:19 to +0800 at 2022-07-01 21:19:26
    From +0800 at 2022-07-01 21:19:26 to +0300 at 2022-07-25 18:20:01
    From +0300 at 2022-07-25 18:30:05 to +0800 at 2022-08-17 17:59:51
    From +0800 at 2022-09-02 20:18:55 to +0300 at 2022-09-08 15:07:00
    From +0300 at 2022-09-08 15:07:00 to +0800 at 2022-09-21 16:15:50
    From +0800 at 2022-10-06 17:00:38 to +0300 at 2022-10-06 21:53:09 (SUSPICIOUS)
    From +0300 at 2022-10-06 21:53:09 to +0800 at 2022-10-23 21:01:08
    From +0800 at 2022-10-23 21:01:08 to +0200 at 2022-11-07 16:24:14
    From +0200 at 2022-11-07 16:24:14 to +0800 at 2022-11-19 23:18:04
    From +0800 at 2023-06-20 20:32:59 to +0300 at 2023-06-27 17:27:09
    From +0300 at 2023-06-27 17:27:09 to +0800 at 2023-06-27 23:38:32 (SUSPICIOUS)
    From +0800 at 2024-02-09 23:59:54 to +0200 at 2024-02-12 17:09:10
    From +0200 at 2024-02-12 17:09:10 to +0800 at 2024-02-13 01:53:33 (SUSPICIOUS)

We can observe that some timezone changes are tagged as ``SUSPICIOUS``.
Jia Tan seems to have traveled at the speed of the light,
and the ``inspect`` command tagged these timezone change, example:

.. code-block::

    From +0300 at 2023-06-27 17:27:09 to +0800 at 2023-06-27 23:38:32 (SUSPICIOUS)

Jia Tan moved from Eastern Europe to Asia in a snap of the fingers.

If we do the same for Lasse or Jonathan (the other persons tagged as
suspicious) in our primary analyze, Jonathan have no suspicious time
change when we run the ``inspect`` command, and Lasse only have one
suspicious time from Asia to Central Europe, but `Lasse is the creator
of xz <https://github.com/tukaani-project/xz/graphs/contributors>`_ so
we can be more confident concerning him and his activity.

But, now let's focus on Jia Tan and let's take a closer look at
the previous results by using the ``investigate`` command:

.. code-block::

    $ defected investiage \
        --file output-from-inspect.csv
    Investigation results saved to 'investigate_results.csv'.
         date_of_change previous_timezone                                              countries_previous current_timezone                                               countries_current                                                        departure                                                          arrival  physically_possible
    2022-10-06 17:00:38             +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore            +0300     Asia, Antarctica, Etc, Europe, Indian, W-SU, Turkey, Africa 2022-10-06 17:00:38 +0800 (time at is 2022-10-06 12:00:38 +0300) 2022-10-06 21:53:09 +0300 (time at is 2022-10-07 02:53:09 +0800)                 True
    2023-06-27 17:27:09             +0300     Asia, Antarctica, Etc, Europe, Indian, W-SU, Turkey, Africa            +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore 2023-06-27 17:27:09 +0300 (time at is 2023-06-27 22:27:09 +0800) 2023-06-27 23:38:32 +0800 (time at is 2023-06-27 18:38:32 +0300)                False
    2024-02-12 17:09:10             +0200            Asia, Libya, EET, Etc, Israel, Europe, Africa, Egypt            +0800 Asia, Antarctica, Hongkong, Etc, PRC, ROC, Australia, Singapore 2024-02-12 17:09:10 +0200 (time at is 2024-02-12 23:09:10 +0800) 2024-02-13 01:53:33 +0800 (time at is 2024-02-12 19:53:33 +0200)                False


.. list-table:: investigate_results.csv
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
     - 2022-10-06 17:00:38 +0800 (time at is 2022-10-06 12:00:38 +0300)
     - 2022-10-06 21:53:09 +0300 (time at is 2022-10-07 02:53:09 +0800)
     - True
   * - 2023-06-27 17:27:09
     - +0300
     - Europe, Turkey, Asia, Africa, Antarctica, Indian, W-SU, Etc
     - +0800
     - Asia, Hongkong, Singapore, Antarctica, Australia, ROC, PRC, Etc
     - 2023-06-27 17:27:09 +0300 (time at is 2023-06-27 22:27:09 +0800)
     - 2023-06-27 23:38:32 +0800 (time at is 2023-06-27 18:38:32 +0300)
     - False
   * - 2024-02-12 17:09:10
     - +0200
     - EET, Europe, Asia, Libya, Israel, Africa, Egypt, Etc
     - +0800
     - Asia, Hongkong, Singapore, Antarctica, Australia, ROC, PRC, Etc
     - 2024-02-12 17:09:10 +0200 (time at is 2024-02-12 23:09:10 +0800)
     - 2024-02-13 01:53:33 +0800 (time at is 2024-02-12 19:53:33 +0200)
     - False

We clearly observe that 2 timezone changes are not possible.

Indeed in these impossible results, if we consider these results
as traveling from Jia Tan, then we can observe that:

* Jia Tan departed from Europe (+0200) at 17:27:09 and arrived in Asia (+0800) at 23:38:32 (18:38:32 at Europe time +0200), hence 1 hour of traveling to travel almost 8000km;
* Jia Tan departed from Asia (+0800) at 17:09:10 and arrived in Europe (+0200) at 01:53:33 (19:53:33 at Asia time +0800), hence, again, 1 hour of traveling to travel almost 8000km;

Conclusion, Jia Tan is so blasting fast.
I want to know the name of his airline!

Interpretation
--------------

The results show that **Jia Tan** also known as `JiaT75
<https://github.com/JiaT75>`_:

* Contributed 449 commits to the repository.
* Operated from **3 different timezones** during his activity period.
* Exhibited **14 timezone changes**, exceeding the threshold of 2,
  which flags them as "suspicious."

These irregular patterns warrant further investigation and could
have raised red flags before the backdoor was merged.

Obviously not all activities are not suspicious. The result above
also show legit activity like the ones from Lasse and Jonathan.
But the one from Jia as been proven to be security attack lead
through `social engineering
<https://en.wikipedia.org/wiki/Social_engineering_(security)>`_.

Lessons Learned
---------------

This case highlights the importance of monitoring contributor
activity, especially in critical open source projects.

By using tools like Defected, maintainers can:

#. Proactively identify suspicious contributors.
#. Investigate anomalies in commit patterns.
#. Prevent security risks, such as backdoors, before they impact
   end users.

Why This Matters
----------------

The case of **Jia Tan (JiaT75)** is a reminder that even trusted
repositories can be compromised. Open source maintainers need tools
like Defected to protect their projects from potential threats by
identifying early warning signs such as irregular timezone changes.

Obviously, not all timezone changes are suspicious, many of them
are legit, but like demonstrated by xz example some are real attempts.
**JiaT75** tried to show that he was located in Asia where some
timezone changes reflect Eastern Europe timezone.

That's like a cold case where a small oversights can reveal
significant details.
