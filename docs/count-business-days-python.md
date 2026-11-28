# Count business days in Python (US federal and NYSE calendars)

This guide shows how to count US business days, add N business days to a date, and check whether a date is a business day, using `usbizdays`. It has no dependencies and no data files. It covers three calendars: `federal` (default), `nyse` and `fed` (Federal Reserve Banks). For the holiday rules themselves, see [US federal holidays: dates and rules](us-federal-holiday-rules.md).

All output below was produced by running the code from the `free/` folder with `PYTHONPATH=src python3`.

## Is this date a business day?

```python
from datetime import date
from usbizdays import is_business_day, holiday_name

print(is_business_day("2026-11-26"))
print(holiday_name("2026-11-26"))
print(is_business_day(date(2026, 7, 3)), holiday_name("2026-07-03"))
```

```
False
Thanksgiving Day
False Independence Day (observed)
```

Dates can be `datetime.date` objects, ISO strings (`YYYY-MM-DD`), or `datetime` objects (including pandas `Timestamp`), which are reduced to their calendar date; results are `date` objects. A weekend or an observed holiday is not a business day. `holiday_name` returns `None` for dates that are not holidays.

## Add N business days

```python
from usbizdays import add_business_days

print(add_business_days("2026-11-25", 3))
print(add_business_days("2026-11-25", -3))
print(add_business_days("2026-11-28", 0))
```

```
2026-12-01
2026-11-20
2026-11-30
```

Thanksgiving (Nov 26) is skipped, and so is the weekend. A negative `n` moves back. With `n = 0`, a non-business day rolls forward to the next business day (Saturday Nov 28 becomes Monday Nov 30).

## Count business days between two dates

```python
from usbizdays import business_days_between

print(business_days_between("2026-11-01", "2026-12-01"))
print(business_days_between("2026-12-01", "2026-11-01"))
print(business_days_between("2026-01-01", "2027-01-01"))
```

```
19
-19
250
```

The start date is included and the end date is excluded. If the end is before the start, the result is negative.

## Command line

```
$ PYTHONPATH=src python3 -m usbizdays add 2026-11-25 3
2026-12-01
$ PYTHONPATH=src python3 -m usbizdays --calendar nyse is 2026-04-03
no (Good Friday)
```

## NYSE vs federal holidays

Set `calendar="nyse"` to count NYSE trading days (supported from 2000). Searching for "NYSE holidays" often turns up the federal list, but the two differ:

```python
from usbizdays import is_business_day, holiday_name

for cal in ("federal", "nyse", "fed"):
    print(cal,
          is_business_day("2026-04-03", calendar=cal),  # Good Friday
          is_business_day("2026-10-12", calendar=cal),  # Columbus Day
          is_business_day("2026-11-11", calendar=cal),  # Veterans Day
          holiday_name("2026-04-03", cal))
```

```
federal True False False None
nyse False True True Good Friday
fed True False False None
```

As the code models them:

- Good Friday: NYSE closed; federal and Federal Reserve open.
- Columbus Day and Veterans Day: NYSE open; federal and Federal Reserve closed.
- Juneteenth: NYSE from 2022 (federal from 2021).
- A Saturday January 1 is not observed on December 31 by NYSE, but is by the federal calendar. The `fed` calendar does not move any Saturday holiday.
- The package does not model NYSE early closes (1:00 pm ET); they are listed in `sample/nyse_early_closes_2026_2027.csv`. Unscheduled closures cannot be predicted.

NYSE example:

```python
from usbizdays import add_business_days, business_days_between

print(add_business_days("2026-11-25", 1, calendar="nyse"))
print(business_days_between("2026-04-01", "2026-04-10", calendar="nyse"),
      business_days_between("2026-04-01", "2026-04-10"))
```

```
2026-11-27
6 7
```

The first line is the day after Thanksgiving (a trading day, closing early). The second shows 6 NYSE days vs 7 federal days in a window that contains Good Friday.

## Compare: numpy.busday_count with a holiday list

NumPy has `busday_count`, `busday_offset` and `is_busday`, which take a list of holidays. You supply the list. This example builds the 2026 list from `usbizdays` (it does not cover other years, which you would add), then checks that NumPy gives the same answers (numpy 2.5.3):

```python
from datetime import date, timedelta
import numpy as np
from usbizdays import holiday_name, business_days_between, add_business_days, is_business_day

d, holidays = date(2026, 1, 1), []
while d.year == 2026:
    if holiday_name(d):
        holidays.append(d.isoformat())
    d += timedelta(days=1)

print(np.busday_count("2026-11-01", "2026-12-01", holidays=holidays))
print(business_days_between("2026-11-01", "2026-12-01"))
print(np.busday_offset("2026-11-25", 3, holidays=holidays))
print(add_business_days("2026-11-25", 3))
print(np.is_busday("2026-11-26", holidays=holidays))
print(is_business_day("2026-11-26"))
print(np.busday_count("2026-11-01", "2026-12-01"))
```

```
19
19
2026-12-01
2026-12-01
False
False
21
```

The last line shows NumPy without a holiday list: 21, because it does not know about Veterans Day (Nov 11) and Thanksgiving (Nov 26). `usbizdays` builds the holiday list for you, for any year, and has the NYSE and Federal Reserve rules.

## Paid full set

The [US federal, NYSE and Fed calendar full set](https://buy.polar.sh/polar_cl_oW9ytw22HhxLxOnke3W8ibcgTXepc2hYuAEyl1gTqqB?utm_source=github&utm_medium=readme&utm_campaign=B&utm_content=us-federal-calendar) ($15, one-time; Polar is the merchant of record and handles sales tax) is the same data as ready-to-load tables, if you would rather not depend on a library:

- Federal holidays 1971-2050 and business days 2000-2050 (CSV + JSON)
- NYSE trading calendar 2000-2050 with early closes and previous/next trading day
- Federal Reserve Bank holidays 2000-2050
- SQLite database, a tested PostgreSQL load script and 80 .ics files
- `bizdays.py` (standard library only) with `is_business_day`, `add_business_days`, `business_days_between`

It is also in the [calendar data bundle](https://buy.polar.sh/polar_cl_HiUeTqJE1gUqHdb3OlOWb6Jml7pdq8E71O2pA4Y9iQ3?utm_source=github&utm_medium=readme&utm_campaign=BUNDLE&utm_content=us-federal-calendar) (US business-day calendar, date dimension and time zone packs) for $35 instead of $49. Full contents: [README](../README.md#full-set-15-one-time).

---

Made by Plainfold. Written with AI assistance. Not legal advice; check OPM for official schedules.
