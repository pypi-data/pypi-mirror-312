Algoseek Connector
==================

[![Documentation Status](https://readthedocs.org/projects/algoseek-connector/badge/?version=latest)](https://algoseek-connector.readthedocs.io/en/latest/?badge=latest) [![Pull request](https://github.com/algoseekgit/algoseek-connector/actions/workflows/pr.yml/badge.svg)](https://github.com/algoseekgit/algoseek-connector/actions/workflows/pr.yml)

A library to fetch and query data from Algoseek datasets using SQL-like queries. The library provides an easy-to-use
pythonic interface to algoseek datasets with custom data filtering/selection. The following query operations
on datasets are supported:

- Selecting columns and arbitrary expressions based on columns
- Filtering by column value/column expression
- Grouping by column(s)
- Sorting by column(s)
- All common arithmetic, logical operations on dataset columns and function application
- Fetching query results as a pandas DataFrame

## Installation

`algoseek-connector` is available on the Python Package Index. Install it using the `pip` command:

    pip install algoseek-connector

More detailed information is available in the getting started page in the library documentation.

## Documentation

Documentation is available [here](https://algoseek-connector.readthedocs.io/en/latest/index.html).

## Getting help

You can contact [Algoseek support](mailto:support@algoseek.com) or check the [project discussions](https://github.com/algoseekgit/algoseek-connector/discussions)

## Reporting an issue

Your feedback is essential for improving Algoseek connector and making it more reliable.
If you encounter a problem or bug, please report it using the repository's
[issue tracker](https://github.com/algoseekgit/algoseek-connector/issues).

Before submitting a new issue, please search the issue tracker to see if the problem has already been reported.

If your question is about how to achieve a specific task or use the library in a certain way, we recommend
posting it in the GitHub Discussions section, rather than the issue tracker.

When reporting an issue, it's helpful to include the following details:

- A code snippet that reproduces the problem.
- If an error occurs, please include the full traceback.
- A brief explanation of why the current behavior is incorrect or unexpected.

For guidance on how to write a clear and effective issue report, refer to this [post](https://matthewrocklin.com/minimal-bug-reports).
