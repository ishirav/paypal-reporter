PayPal Reporter
===============

A python library to generate reports about activity in a PayPal account.
Currently supports listing transactions from the previous month.

I was looking for a way to get scheduled monthly summaries from PayPal, but could not find an existing solution.
So I created this project, which retrieves transaction information via PayPal's NVP API.

*NOTE: This module is not created by, endorsed by, or in any way affiliated with PayPal.*

Installation
------------

To install paypal_reporter::

    pip install paypal_reporter


Usage
-----

To get a printout of the transactions from the previous month, first create a json file containing your PayPal account's credentials::

    {
        "USER": "...",
        "PWD": "...",
        "SIGNATURE": "..."
    }

Then run::

    python -m paypal_reporter.transactions <path-to-credentials-file>


Limitations
-----------

PayPal's API returns a maximum of 100 transactions. Currently this library does not handle pagination, therefore
only 100 transactions are retrieved.


Dependencies
------------

- `requests <http://docs.python-requests.org/>`_
- `tabulate <https://pypi.python.org/pypi/tabulate>`_


API
---

The following methods are defined in ``paypal_reporter.transactions`` and can be used to create your own reports.

get_transactions(credentials, start_datetime, end_datetime)
    Gets the list of transactions from PayPal in the given date range. ``credentials`` should be a dictionary containing
    ``USER``, ``PWD`` and ``SIGNATURE``. Returns a list of dicts, sorted by ascending timestamp. In case
    of a problem the method raises ``paypal_reporter.transactions.PayPalError``.

print_transactions(txns, format='simple', columns=DEFAULT_COLUMNS)
    Given a list of transaction dicts, this method formats them using the ``tabulate`` library and prints then to
    stdout. ``format`` could be any format supported by ``tabulate``, such as plain / simple / html / tsv. ``columns``
    is a list of column names to take from the transaction dicts. The default columns are TIMESTAMP, TRANSACTIONID,  
    STATUS, TYPE, NAME, AMT, FEEAMT, NETAMT, and CURRENCYCODE.

