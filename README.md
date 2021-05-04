# CVE Bot: Telegram bot that notifies about package update linked with CVE

[![Build Status](https://travis-ci.com/weastur/cve_bot.svg?branch=main)](https://travis-ci.com/weastur/cve_bot)
[![codecov](https://codecov.io/gh/weastur/cve_bot/branch/main/graph/badge.svg)](https://codecov.io/gh/weastur/cve_bot)
[![PyPi version](https://img.shields.io/pypi/v/cve_bot.svg)](https://pypi.org/project/cve_bot/)
[![Python versions](https://img.shields.io/pypi/pyversions/cve_bot)](https://pypi.org/project/cve_bot/)
[![black-formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Try it out!](https://t.me/packages_cve_bot)

## Key Features

* Frequent DB update 
* Get actual info based on CVE number or Package name
* Subscribe to update at any number of CVEs

## Technical Requirements/Installation

### Pre-requirements
Install Python 3.9, and pip package management tool.

## Development Status

CVE Bot is in active development and accepts contributions. See our [Contributing](#how-to-contribute) section below for more details.

We report new releases information [here](https://github.com/weastur/cve_bot/releases).

## How to contribute

Fork, clone, setup development environment. **No third-party build or test tools** need to be installed at your system.

```shell
python3 -m venv .venv
. ./.venv/bin/activate
pip install setuptools wheel
pip install -e '.[dev]'
```

After that you'll have cve_bot and all development tools installed into virtualenv. Refer to [config](./cve_bot/config.py) 
to set proper env vars for development. Actually the minimum required is `CVE_BOT_TOKEN` with your token
Hack, then make PR. Don't forget to write unit tests, and check your code:

```shell
flake8 cve_bot
isort -c cve_bot
black --check cve_bot
pytest --cov
```

Or you can just install git-hooks

### Git hooks

```shell
ln -s -r -t ./.git/hooks/ ./hooks/*
```

## License

MIT, see [LICENSE](./LICENSE).