# defected

![Build](https://github.com/4383/defected/actions/workflows/main.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/defected.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/defected.svg)
![PyPI - Status](https://img.shields.io/pypi/status/defected.svg)
[![Downloads](https://pepy.tech/badge/defected)](https://pepy.tech/project/defected)
[![Downloads](https://pepy.tech/badge/defected/month)](https://pepy.tech/project/defected/month)

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

We can think of Defected as an [OSINT](
https://en.wikipedia.org/wiki/Open-source_intelligence) tool that
can used by project maintainers to fight against social engineering.

Visit the [official documentation](https://defected.readthedocs.io/).

## Install

```
$ pip install defected
```

## Usage

```
$ defected -h
```

Examples of usage and documentation of available commands are
available in the [official documentation](https://defected.readthedocs.io/).

## The Problem

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

## Goal

The goal of defected is to highlight potential
social engineering threats.

Defected addresses these challenges by:
- **Detecting frequent timezone changes** in commit metadata.
- **Highlighting contributors** with irregular commit patterns.
- **Flagging potential risks** for maintainers to investigate.
- Providing **clear and exportable reports** for further analysis.

## Features

1. **Easy-to-Use CLI**:
   - Installable via PyPI, Defected is simple to run directly from your
     terminal.
2. **Commit Metadata Analysis**:
   - Extracts author, email, date, and timezone data from Git logs.
3. **Timezone Change Detection**:
   - Flags contributors exceeding a configurable threshold of timezone
     changes.
4. **Reveal Deception**:
   - Find fraudulous activity and unveil bad intentions ([example](
     https://defected.readthedocs.io/en/latest/examples/investigations/xz-utils-backdoor.html)).
5. **Customizable Options**:
   - Adjust thresholds, filter suspicious results.
6. **Exportable Reports**:
   - Saves results in CSV format for further analysis.

## Contributing

We welcome contributions to Defected!

To contribute:
1. Fork the repository;
2. Create a feature branch;
3. Introduce your changes;
4. Submit a pull request with a detailed description of your changes.

## License

Defected is licensed under the MIT License. See the `LICENSE`
file for details.

## Acknowledgments

This project is inspired by the open source community and aims to
empower maintainers with tools to ensure project security and integrity.
