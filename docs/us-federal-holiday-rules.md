# US federal holidays: dates, observance rules and 2026-2027 calendar

This guide lists the 11 US federal holidays under 5 U.S.C. 6103, how each date is set, and how a holiday that lands on a weekend is moved. It also shows how the free `usbizdays` Python package models these rules. If you searched for "US federal holidays 2027", the table below has the observed dates.

## The 11 holidays and their date rules

| Holiday | Date rule | Notes |
|---|---|---|
| New Year's Day | January 1 | |
| Birthday of Martin Luther King, Jr. | Third Monday of January | Package: from 1986 |
| Washington's Birthday | Third Monday of February | Often called Presidents Day |
| Memorial Day | Last Monday of May | |
| Juneteenth National Independence Day | June 19 | Package: from 2021 only |
| Independence Day | July 4 | |
| Labor Day | First Monday of September | |
| Columbus Day | Second Monday of October | |
| Veterans Day | November 11 | Package: fourth Monday of October in 1971-1977, November 11 from 1978 |
| Thanksgiving Day | Fourth Thursday of November | |
| Christmas Day | December 25 | |

Rules checked against `src/usbizdays/federal.py`.

## Weekend observance rule

When a holiday falls on a weekend, federal employees get a nearby weekday instead:

- Saturday: observed the Friday before.
- Sunday: observed the Monday after.

Holidays set as a Monday or Thursday never fall on a weekend. The date-based ones can: New Year's Day, Juneteenth, Independence Day, Veterans Day and Christmas.

Example: Independence Day 2026 is Saturday, July 4, so it is observed Friday, July 3.

```
$ PYTHONPATH=src python3 -m usbizdays is 2026-07-03
no (Independence Day (observed))
```

## Juneteenth from 2021

Juneteenth National Independence Day (June 19) became a federal holiday in 2021. The package includes it from 2021 on. In 2027 it falls on a Saturday, so it is observed Friday, June 18.

## When January 1 falls on a Saturday

The Friday before is December 31 of the prior year. The package follows OPM practice and observes New Year's Day on that December 31. New Year's Day 2028 is a Saturday, so the observed date is Friday, 2027-12-31 (see `sample/federal_holidays.csv`, 2028 row).

```
$ PYTHONPATH=src python3 -c "from usbizdays import *; print(holiday_name('2027-12-31'), is_business_day('2027-12-31'))"
New Year's Day (observed) False
```

This applies to the federal-employee calendar. The package's NYSE calendar does not do this: the exchange stays open on a December 31 that follows a Saturday January 1. The Federal Reserve calendar in the package also does not move any Saturday holiday to Friday.

## Inauguration Day

Inauguration Day (January 20, every four years) is a holiday only for federal employees in the Washington, DC area. The package does not include it: there is no Inauguration Day entry in `federal.py`, and the README lists it under "Not included". In 2025, January 20 was also Martin Luther King, Jr. Day, so the package marks it as a holiday for that reason only:

```
$ PYTHONPATH=src python3 -c "from usbizdays import *; print(is_business_day('2025-01-20'), holiday_name('2025-01-20'))"
False Birthday of Martin Luther King, Jr.
```

In 2029, January 20 is a Saturday, and the package treats it as an ordinary weekend day. January 20, 2033 is a Thursday and shows as a business day (`True`).

If you need DC-area federal closures, add that date yourself.

## Observed dates for 2026 and 2027

Copied from `sample/federal_holidays.csv`.

### 2026

| Holiday | Actual date | Observed date | Observed weekday |
|---|---|---|---|
| New Year's Day | 2026-01-01 | 2026-01-01 | Thursday |
| Birthday of Martin Luther King, Jr. | 2026-01-19 | 2026-01-19 | Monday |
| Washington's Birthday | 2026-02-16 | 2026-02-16 | Monday |
| Memorial Day | 2026-05-25 | 2026-05-25 | Monday |
| Juneteenth National Independence Day | 2026-06-19 | 2026-06-19 | Friday |
| Independence Day | 2026-07-04 | 2026-07-03 | Friday |
| Labor Day | 2026-09-07 | 2026-09-07 | Monday |
| Columbus Day | 2026-10-12 | 2026-10-12 | Monday |
| Veterans Day | 2026-11-11 | 2026-11-11 | Wednesday |
| Thanksgiving Day | 2026-11-26 | 2026-11-26 | Thursday |
| Christmas Day | 2026-12-25 | 2026-12-25 | Friday |

### 2027

| Holiday | Actual date | Observed date | Observed weekday |
|---|---|---|---|
| New Year's Day | 2027-01-01 | 2027-01-01 | Friday |
| Birthday of Martin Luther King, Jr. | 2027-01-18 | 2027-01-18 | Monday |
| Washington's Birthday | 2027-02-15 | 2027-02-15 | Monday |
| Memorial Day | 2027-05-31 | 2027-05-31 | Monday |
| Juneteenth National Independence Day | 2027-06-19 | 2027-06-18 | Friday |
| Independence Day | 2027-07-04 | 2027-07-05 | Monday |
| Labor Day | 2027-09-06 | 2027-09-06 | Monday |
| Columbus Day | 2027-10-11 | 2027-10-11 | Monday |
| Veterans Day | 2027-11-11 | 2027-11-11 | Thursday |
| Thanksgiving Day | 2027-11-25 | 2027-11-25 | Thursday |
| Christmas Day | 2027-12-25 | 2027-12-24 | Friday |

Observed dates in the free sample: [`sample/federal_holidays.csv`](../sample/federal_holidays.csv) (2024-2028). Calendar files for 2026 and 2027 are in [`sample/ics/`](../sample/ics/).

## Check a date in Python

```
$ PYTHONPATH=src python3 -m usbizdays holidays 2027
2027-01-01 New Year's Day
2027-01-18 Birthday of Martin Luther King, Jr.
2027-02-15 Washington's Birthday
2027-05-31 Memorial Day
2027-06-18 Juneteenth National Independence Day (observed)
2027-07-05 Independence Day (observed)
2027-09-06 Labor Day
2027-10-11 Columbus Day
2027-11-11 Veterans Day
2027-11-25 Thanksgiving Day
2027-12-24 Christmas Day (observed)
2027-12-31 New Year's Day (observed)
```

The last line is New Year's Day 2028, observed in 2027. See the companion guide [Count business days in Python](count-business-days-python.md).

## Paid full set

A paid full set exists with federal holidays 1971-2050 and more calendars (NYSE, Federal Reserve). The contents are described in [../README.md](../README.md).

---

Made by Plainfold. Written with AI assistance. Not legal advice; check OPM for official schedules.
