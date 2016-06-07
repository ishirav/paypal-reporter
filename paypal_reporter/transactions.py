import requests
import urlparse
import re
import sys
import json
from tabulate import tabulate
from collections import defaultdict
from datetime import datetime, date, timedelta

requests.packages.urllib3.disable_warnings()


PAYPAL_URL = 'https://api-3t.paypal.com/nvp'
PAYPAL_VERSION = '124'
DEFAULT_COLUMNS = 'TIMESTAMP TRANSACTIONID STATUS TYPE NAME AMT FEEAMT NETAMT CURRENCYCODE'.split()


class PayPalError(Exception):
    pass


def send_request(credentials, start_datetime, end_datetime):
    '''
    Sends a TransactionSearch request to PayPal and returns the 
    raw fields. Raises an exception in case the request fails or
    PayPal reports an error.
    '''
    data = dict(
        credentials,
        VERSION=PAYPAL_VERSION,
        METHOD='TransactionSearch',
        STARTDATE=start_datetime.isoformat() + 'Z',
        ENDDATE=end_datetime.isoformat() + 'Z'
    )
    r = requests.get(PAYPAL_URL, data)
    r.raise_for_status()
    raw = _unlistify(urlparse.parse_qs(r.content))
    raise_for_error(raw)
    return raw


def _unlistify(raw):
    '''
    Converts a dictionary of lists into a dictionary of scalars by
    taking the first item from each list. 
    '''
    return {k: v[0] for k, v in raw.iteritems()}


def raise_for_error(raw):
    '''
    Raises a PayPalError in case the response fields contain an error code.
    '''
    if 'L_ERRORCODE0' in raw:
        msg = '[%(L_ERRORCODE0)s] %(L_SHORTMESSAGE0)s %(L_LONGMESSAGE0)s' % raw
        raise PayPalError(msg)


def collect_transactions(raw):
    '''
    Converts the raw transaction info returned by PayPal into a list
    of transactions. Each item on the list is a dict, and the list is
    sorted by ascending timestamp.
    '''
    # The raw keys are indexed (e.g. L_AMT0, L_AMT1 etc.) so first
    # collect them into a dict of dicts, keyed by the index
    txns_dict = defaultdict(dict)
    for key, val in raw.iteritems():
        name, index = _parse_key(key)
        if name:
            if name == 'TIMESTAMP':
                val = val[:-1].replace('T', ' ')
            txns_dict[index][name] = val
    # Convert into a list of dicts
    txns_list = []
    for key in reversed(sorted(txns_dict.keys())):
        txns_list.append(txns_dict[key])
    return txns_list


def _parse_key(s):
    '''
    Parses an indexed key into its parts, For example 'L_AMT7' ==> ('AMT', 7).
    In case the key does not match the expected format, returns (None, None).
    '''
    m = re.match(r'L_(\D+)(\d+)', s)
    return (m.group(1), int(m.group(2))) if m else (None, None)


def get_transactions(credentials, start_datetime, end_datetime):
    '''
    Gets the list of transactions from PayPal.
    '''
    return collect_transactions(send_request(credentials, start_datetime, end_datetime))


def print_transactions(txns, format='simple', columns=DEFAULT_COLUMNS):
    '''
    Prints the given list of transactions in tabular format.
    '''
    table = []
    for txn in txns:
        table.append([txn.get(col) for col in columns])
    print tabulate(table, columns, floatfmt=".2f", tablefmt=format)


def _date_range():
    '''
    Returns a tuple (start_datetime, end_datetime) covering the previous month. 
    '''
    d = date.today()
    end_datetime = datetime(d.year, d.month, 1) - timedelta(days=1)
    start_datetime = end_datetime.replace(day=1)
    end_datetime += timedelta(hours=23, minutes=59, seconds=59)
    return (start_datetime, end_datetime)   


if __name__ == '__main__':
    with open(sys.argv[1]) as fd:
        credentials = json.load(fd)
    start_datetime, end_datetime = _date_range()
    txns = get_transactions(credentials, start_datetime, end_datetime)
    print_transactions(txns)
