.. defected documentation master file, created by
   sphinx-quickstart on Thu Nov 28 18:37:01 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

defected documentation
======================

**Defected is a CLI tool designed to analyze Git logs and detect
suspicious behaviors, such as frequent timezone changes, to enhance
the security and reliability of open-source projects.**

Open source projects thrive on collaboration, but their openness
comes with risks. Contributors may unknowingly or intentionally
exhibit suspicious behaviors, such as:
- Frequent timezone changes in their commit metadata.
- Working at unusual hours or during public holidays.
- Unusual patterns in commit activity.

These anomalies could indicate automation scripts, compromised
accounts, or malicious actions.

**Defected** is a CLI tool designed to help maintainers detect and flag
suspicious commit patterns. By analyzing Git logs, Defected provides
insights into contributors’ behaviors, helping ensure the security
and integrity of your project.

We can think of Defected as an `OSINT
<https://en.wikipedia.org/wiki/Open-source_intelligence>`_ tool that
can used by project maintainers to fight against social engineering.

Install
-------

.. code-block::

    $ pip install defected

The Problem
-----------

Most open source projects rely on volunteers, but not all
volunteers are all well intentioned. Strategic, financial, or
again geopolical aspect made that some actors seek to profit
from open source project to carry out their hidden agenda.

Bad actors have interest in open source to introduce exploits,
backdoors, or payloads, or even to scuttle projects.

It expose users of open source projects to threats. Such kind
of social engineering can lead users to data leak, invasion of
privacy, and lot nightmare scenarios.

As maintainers of these projects we are responsible of the safety
of people that who trusted in our work.

Usage
-----

Defected comes with various commands. Those commands can be
used in coordination to investigate a specific scenario.

Please find more details about the available commands:

.. toctree::
   :maxdepth: 1
   :glob:

   commands/*

What are the signs of a bad actor activity?
-------------------------------------------

Many kind of signs can reveal bad actor activity, here are
some few examples:

- the intentional removal of security feature/config by a contributor;
- someone that stole a github account to steal identity of someone else
  and get access to the code base of a critical software (think
  of vlc, xz, ssh, etc);
- someone that travel faster than light (strange timezone behaviours).

Defected is focused on the identification of use case related to this
last example.

Why timezone matters?
---------------------

Timezone matters because they are an indicator that can
reveal strange behaviours.
On open source project timezone used by contributors are publics,
so their history can reveal patterns and so timezone can reveal
suspicious behaviours.

In other words, timezone can used as an entry point for `OSINT
<https://en.wikipedia.org/wiki/Open-source_intelligence>`_
investigations.

Here is some examples of patterns that timezone can reveal:

1. **Frequent timezone changes**: automation scripts or account misuse
   can result in rapid changes in timezone metadata;
2. **Unusual working hours**: commits made during public holidays or
   odd hours may indicate suspicious activity;
3. **Behavioral anomalies**: patterns of activity inconsistent with
   normal contributor behavior could point to automation or malicious
   intent.

Obvisously not all timezone changes are suspicious, by example:

- bots or workers that commit or merge changes are surely
  spreads on various servers with various timezone;
- many open source contributors travel at conference and so their
  timezone can be automatically updated by their environment. By
  example desktop environment like KDE, gnome, etc can automatically
  set your timezone.

But in the middle of the legit scenarios, some are suspicious for real,
and observing a real contributor traveling at the speed of the light
due to a fake identity can reveal bad intentions.

Manually detecting these patterns is tedious and impractical for large
projects, this is why we created defected.

defected’s Solution
-------------------

We implemented defected with the following statement in mind:

> If contributor timezone move weirdly then that could indicate
> that this user is trying to hide is activity and his identity.
> If a user show timezone changes that are not logic or physically
> possible then that could indicate something weird and we should be
> more careful with the changes proposed by that contributor.

Defected addresses these challenges by automating git log analyze.
Defected automatically extract these weird patterns and give you
a report.

Defected show you who are these contributors. Defected highlight
illogical timezone changes. Defected allow you to investigate
the patterns of these suspicious contributors, like working hours
countries, etc.

Defected raise your awarness and allow you better protect the project
you cherish.

Real Use Cases Examples
-----------------------

Each 3 months a new `CVE
<https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures>`_
with the highest `CVSS <https://en.wikipedia.org/wiki/Common_Vulnerability_Scoring_System>`_ score (10.0) is discovered.

We can run a post-mortem investigation with defected to see if it
reveal something that the well know stories already revealed us?

Here are investigation made with defected on real use cases:

.. toctree::
   :maxdepth: 1
   :glob:

   examples/investigations/*
