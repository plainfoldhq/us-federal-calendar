#!/usr/bin/env python3
"""usbizdays: US federal, NYSE and Federal Reserve business-day helper (Python 3 standard library only). MIT license.

Rule-based (weekend = Sat/Sun), so it works for any year in range, with no data files.

Calendars: "federal" (default; federal employees, 5 U.S.C. 6103), "nyse"
(NYSE trading days, from 2000), "fed" (Federal Reserve Banks, from 2000;
Saturday holidays not moved).

Library:
    from usbizdays import is_business_day, add_business_days, business_days_between
    is_business_day("2026-04-03", calendar="nyse")   # False (Good Friday)
CLI:
    usbizdays is 2026-11-27
    usbizdays add 2026-11-25 3        # -> 2026-12-01
    usbizdays between 2026-11-01 2026-12-01
    usbizdays holidays 2027
    usbizdays --calendar nyse add 2026-11-25 1   # -> 2026-11-27
"""
import sys
from datetime import date, datetime, timedelta
from functools import lru_cache

from . import federal as g
from . import markets


@lru_cache(maxsize=None)
def _observed_in(year):
    """Observed holiday dates that fall in calendar year `year`, with names."""
    out = {}
    for y in (year, year + 1):  # Jan 1 of next year can be observed Dec 31
        if y < 1971:
            continue
        for name, _slug, d in g.holidays_for_year(y):
            o = g.observed(d)
            if o.year == year:
                out[o] = name + (" (observed)" if o != d else "")
    return out


@lru_cache(maxsize=None)
def _closed_in(calendar, year):
    if calendar not in ("federal", "nyse", "fed"):
        raise ValueError("calendar must be federal, nyse or fed")
    if calendar == "federal":
        return _observed_in(year)
    if year < 2000:
        raise ValueError("nyse and fed calendars are implemented from 2000 on")
    if calendar == "nyse":
        return markets.nyse_holidays(year)
    if calendar == "fed":
        return markets.fed_holidays(year)
    raise ValueError("calendar must be federal, nyse or fed")


def _d(x):
    if isinstance(x, datetime):  # also pandas Timestamp; compare by calendar date
        return x.date()
    return x if isinstance(x, date) else date.fromisoformat(x)


def holiday_name(d, calendar="federal"):
    d = _d(d)
    return _closed_in(calendar, d.year).get(d)


def is_business_day(d, calendar="federal"):
    d = _d(d)
    if d.year < 1971:
        raise ValueError("rules implemented from 1971 on")
    return d.weekday() < 5 and d not in _closed_in(calendar, d.year)


def add_business_days(d, n, calendar="federal"):
    """Move n business days forward (n > 0) or back (n < 0). n = 0 rolls a
    non-business day forward to the next business day."""
    d = _d(d)
    step = 1 if n >= 0 else -1
    if n == 0:
        while not is_business_day(d, calendar):
            d += timedelta(days=1)
        return d
    left = abs(n)
    while left:
        d += timedelta(days=step)
        if is_business_day(d, calendar):
            left -= 1
    return d


def business_days_between(start, end, calendar="federal"):
    """Business days in [start, end) - start included, end excluded."""
    s, e = _d(start), _d(end)
    sign = 1
    if e < s:
        s, e, sign = e, s, -1
    n, d = 0, s
    while d < e:
        n += is_business_day(d, calendar)
        d += timedelta(days=1)
    return sign * n


def main(argv):
    cal = "federal"
    if len(argv) > 2 and argv[1] == "--calendar":
        cal = argv[2]
        argv = argv[:1] + argv[3:]
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        return _run(argv, cal)
    except (IndexError, ValueError) as e:
        print("error: %s" % (e if isinstance(e, ValueError) else "missing argument"), file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2


def _run(argv, cal):
    cmd = argv[1]
    if cmd == "is":
        d = _d(argv[2])
        nm = holiday_name(d, cal)
        print("yes" if is_business_day(d, cal) else "no" + (" (%s)" % nm if nm else ""))
    elif cmd == "add":
        print(add_business_days(argv[2], int(argv[3]), cal).isoformat())
    elif cmd == "between":
        print(business_days_between(argv[2], argv[3], cal))
    elif cmd == "holidays":
        for d, nm in sorted(_closed_in(cal, int(argv[2])).items()):
            print(d.isoformat(), nm)
    else:
        print(__doc__)
        return 2
    return 0


def cli():
    sys.exit(main(sys.argv))


if __name__ == "__main__":
    cli()
