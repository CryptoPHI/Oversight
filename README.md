# Oversight

An all-powerful tool-set for MonetraryUnit

[![Build Status](https://travis-ci.org/CryptoPHI/Oversight.svg?branch=master)](https://travis-ci.org/CryptoPHI/Oversight)

Oversight is an autonomous agent for a persistent processing and automation Layer for MonetaryUnit Core tasks, and a base for functions expansion in preparation for the move to "DASH Evolution" codebase derivatives as and when released.

Oversight "P" is implemented as a Python application while  Oversight "C" is implemented as a C++ application; both bind to a local MonetaryUnit instance and extends its operational scope.

This guide covers Oversight deployment onto Ubuntu +14.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python-virtualenv

Make sure the local MonetaryUnit daemon running is of suitable version:

    $ mue-cli getinfo | grep version

### 2.a Install Oversight "P"

Clone the Oversight repo and install Python dependencies.

    $ git clone https://github.com/CryptoPHI/Oversight.git && cd Oversight
    $ virtualenv ./OversightP
    $ ./OversightP/bin/pip install -r requirements.txt

### 3. Set up Cron

Set up a crontab entry to call Oversight every minute:

    $ crontab -e

In the crontab editor, add the lines below:
    
    * * * * * cd /[path you cloned Oversight in]/Oversight && ./OversightP/bin/python bin/Oversight.py >/dev/null 2>&1
    
  or: with logging as a basic user
    
    * * * * * cd /[path you cloned Oversight in]/Oversight && ./OversightP/bin/python bin/Oversight.py >/dev/null 2>&1  2>&1 >> /[path to user home]/oversight.log 2>&1
    
  or: with logging as root
    
    * * * * * cd /[path you cloned Oversight in]/Oversight && ./OversightP/bin/python bin/Oversight.py >/dev/null 2>&1  2>&1 >> /var/log/oversight.log 2>&1

### 4. Test the Configuration

Test the config by runnings all tests from the Oversight folder you cloned into

    $ ./OversightP/bin/py.test ./test

With all tests passing and crontab setup, Oversight will stay in sync with MonetaryUnit instance and the installation is complete.

## Configuration

An alternative (non-default) path to the `mue.conf` file can be specified in `Oversight.conf`:

    coin_conf=/path/to/mue.conf

## Troubleshooting

To view debug output, set the `Oversight_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ Oversight_DEBUG=1 ./OversightP/bin/python bin/Oversight.py

### License

Released under the MIT license, under the same terms as DashCore and MoneytaryUnit core. See [LICENSE](LICENSE) for more info.
