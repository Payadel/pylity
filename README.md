<div align="center">
  <h1>pylity</h1>
  <br />
  <a href="#getting-started"><strong>Getting Started »</strong></a>
  <br />
  <br />
  <a href="https://github.com/Payadel/pylity/issues/new?assignees=&labels=bug&template=BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/Payadel/pylity/issues/new?assignees=&labels=enhancement&template=FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/Payadel/pylity/issues/new?assignees=&labels=question&template=SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![code with love by Payadel](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-Payadel-ff1414.svg?style=flat-square)](https://github.com/Payadel)

![GitHub](https://img.shields.io/github/license/Payadel/pylity)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/Payadel/pylity/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)

</div>


## About

The `pylity` package is a set of utility and common functions for Python.
**pylity** means `Python Utility`.

When we work on different projects, there are usually functions that are **common** between the projects. Functions that we generally call Utility or helpers or something like that. Functions that are **independent** and can be used in different places.

Well, instead of copying and pasting these functions in a new project every time, it is better to have a package that gathers all these together so that we can install and use them **easily**. This is the goal of this project. :)


## Getting Started

### Installation

Use pip to install package:

```shell
pip install pylity --upgrade
```

## Usage

### Prerequisites

Please note that this package uses [on_rails](https://github.com/payadel/on_rails) package for most functions. `on_rails` is an easy and valuable package for better **error management**. If you are not familiar with this package, you should read its documentation.

### Sample

A set of different functions are grouped into related **classes**.
Import any class you want, then use the functions.
For example:

```python
from pylity import Function

Function.is_func_valid(lambda: None)  # returns True

Function.get_num_of_params(lambda a, b, c: None) \
    .on_success(lambda num_of_params: print(f"Number of parameters is: {num_of_params}")) \
    .on_fail(lambda result: print(f"An error occurred:\n{result}"))
```

## CHANGELOG

Please see the [CHANGELOG](https://github.com/Payadel/pylity/blob/main/CHANGELOG.md) file.

## Roadmap

See the [open issues](https://github.com/Payadel/pylity/issues) for a list of proposed features (and known
issues).

- [Top Feature Requests](https://github.com/Payadel/pylity/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/Payadel/pylity/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/Payadel/pylity/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/Payadel/pylity/issues/new?assignees=&labels=question&template=SUPPORT_QUESTION.md&title=support%3A+)

## Project assistance

If you want to say **thank you** or/and support active development of pylity:

- Add a [GitHub Star](https://github.com/Payadel/pylity) to the project.
- Tweet about the pylity.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your
  personal blog.

Together, we can make pylity **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the free/open-source community such an
amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly
appreciated**.

Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Payadel](https://github.com/Payadel).

For a full list of all authors and contributors,
see [the contributors page](https://github.com/Payadel/pylity/contributors).

## Security

`pylity` follows good practices of security, but 100% security cannot be assured. `pylity` is provided **"as
is"** without any **warranty**.

_For more information and to report security issues, please refer to our [security documentation](docs/SECURITY.md)._

## License

This project is licensed under the **GPLv3**.

See [LICENSE](LICENSE) for more information.
