# US federal holidays, business days and NYSE market holidays (free sample)

[![tests](https://github.com/plainfoldhq/us-federal-calendar/actions/workflows/tests.yml/badge.svg)](https://github.com/plainfoldhq/us-federal-calendar/actions/workflows/tests.yml)

US federal holiday dates with their **observed** dates, plus a day-by-day **business-day calendar**, as CSV and iCalendar (.ics). Generated from 5 U.S.C. 6103 with the standard observance rule: a Saturday holiday is observed the Friday before, a Sunday holiday the Monday after (so New Year's Day 2022 was observed on Friday 2021-12-31).

## Reference pages

Year-by-year tables built from this data: [US federal holidays](https://plainfoldhq.github.io/us-federal-holidays/), [NYSE holidays and early closes](https://plainfoldhq.github.io/nyse-holidays/), [Federal Reserve holidays](https://plainfoldhq.github.io/federal-reserve-holidays/), [business days per month](https://plainfoldhq.github.io/business-days/), and [which holidays close the stock market vs federal offices vs the Fed](https://plainfoldhq.github.io/is-the-stock-market-open-on-holidays/). Outside the US: [holidays of eight more stock exchanges](https://plainfoldhq.github.io/stock-market-holidays/) (LSE, TSX, Xetra, Euronext, Tokyo, HKEX, ASX, SIX), with a [free CSV](https://github.com/plainfoldhq/stock-exchange-holidays).

## Guides

- [US federal holiday rules, observance and 2026-2027 dates](https://github.com/plainfoldhq/us-federal-calendar/blob/main/docs/us-federal-holiday-rules.md)
- [Count business days in Python (federal and NYSE calendars)](https://github.com/plainfoldhq/us-federal-calendar/blob/main/docs/count-business-days-python.md)

## Python package (free)

`usbizdays` answers "is this a business day?" for three US calendars, with no dependencies and no data files: `federal` (federal employees; 5 U.S.C. 6103, from 1971), `nyse` (NYSE trading days, from 2000) and `fed` (Federal Reserve Banks, from 2000; a Saturday holiday is not moved to Friday).

```python
from usbizdays import is_business_day, add_business_days, business_days_between
is_business_day("2026-04-03", calendar="nyse")   # False: Good Friday
is_business_day("2026-04-03", calendar="fed")    # True
add_business_days("2026-11-25", 3)               # date(2026, 12, 1)
business_days_between("2026-11-01", "2026-12-01")  # 19
```

CLI: `usbizdays --calendar nyse holidays 2027`, `usbizdays add 2026-11-25 3`. Install with `pip install usbizdays` or run from a clone with `PYTHONPATH=src python3 -m usbizdays ...`.

Useful for: payroll and settlement date math, SLA and due-date calculations, "next business day" logic, data warehouses that need a date dimension, and calendar imports.

## Free sample (this repo)

| File | Contents |
|---|---|
| `sample/federal_holidays.csv` | All federal holidays 2024-2028: actual date, observed date, weekday |
| `sample/business_days.csv` | Every day of 2026: weekend flag, observed-holiday flag, business-day flag, index in month, business days remaining in month |
| `sample/nyse_closures_2026_2027.csv`, `sample/nyse_early_closes_2026_2027.csv` | NYSE full-day closures and 1:00 pm ET early closes for 2026-2027 |
| `sample/ics/federal_holidays_2026.ics`, `..._2027.ics` | Observed holidays as all-day calendar events (import into Google Calendar, Outlook, Apple Calendar) |

`business_days.csv` columns: `date, is_weekend, is_federal_holiday_observed, is_business_day, business_day_index_in_month, business_days_remaining_in_month`.

## Full set ($15, one-time)

[Buy the full set on Polar](https://buy.polar.sh/polar_cl_oW9ytw22HhxLxOnke3W8ibcgTXepc2hYuAEyl1gTqqB) (Polar is the merchant of record and handles sales tax). It contains:

- Federal holidays 1971-2050 (815 rows, CSV + JSON) and business days 2000-2050 (18,628 rows)
- NYSE trading calendar 2000-2050: every day with open/closed, reason, early closes, previous/next trading day; 490 closures (including Sept 11 2001, Hurricane Sandy, national days of mourning) and 110 early closes
- Federal Reserve Bank holidays 2000-2050 (Saturday holidays are not moved to Friday, unlike the federal-employee calendar)
- Extended business-day table: weekday, holiday name, previous/next business day, business days in month, last-business-day-of-month flag, index in year
- SQLite database with every table, and a tested PostgreSQL load script
- 80 .ics files, one per year
- `bizdays.py` (Python 3 standard library): `is_business_day`, `add_business_days`, `business_days_between`, holidays for any year from 1971, plus a CLI
- The generator scripts and tests

Also sold as part of the [calendar data bundle](https://buy.polar.sh/polar_cl_HiUeTqJE1gUqHdb3OlOWb6Jml7pdq8E71O2pA4Y9iQ3): this pack plus the other two Plainfold calendar data packs (business days, date dimension, time zone transitions) for $35 instead of $49.

## How it was checked

Tests compare against known observed dates. Every observed federal holiday for 1971-2050, and every NYSE closure and early close for 2000-2050, was also compared with the open-source Python [`holidays`](https://pypi.org/project/holidays/) package (v0.108): 0 differences. Not compared row by row with OPM's, NYSE's or the Federal Reserve's own published tables. Future unscheduled market closures cannot be predicted.

## Rules and limits

- Holidays: New Year's Day; Martin Luther King Jr.'s Birthday (from 1986); Washington's Birthday; Memorial Day; Juneteenth (from 2021); Independence Day; Labor Day; Columbus Day; Veterans Day (fourth Monday of October 1971-1977, November 11 from 1978); Thanksgiving; Christmas.
- NYSE (sample and full set): closed on Good Friday, open on Columbus Day and Veterans Day; a Saturday New Year's Day is not observed on December 31.
- Not included: Inauguration Day (Washington, DC area only), state and local holidays, Nasdaq/CME/bond-market schedules, and one-off federal closures by executive order.
- Future years follow current law; Congress can change it. Verify against official sources before legal, payroll or settlement use.

## Related
- [plainfoldhq/date-dimension](https://github.com/plainfoldhq/date-dimension): date dimension table and 4-5-4 / 4-4-5 / 5-4-4 retail calendars (Python package `retailcal`); [full pack on Polar](https://buy.polar.sh/polar_cl_dQIvyRLcbGYoTfZgVmsIENITeo4Zu2zok8JI94KfqWn).
- [plainfoldhq/tz-transitions](https://github.com/plainfoldhq/tz-transitions): IANA time zone transitions 1970-2050 and DST test vectors.
- [plainfoldhq/stock-exchange-holidays](https://github.com/plainfoldhq/stock-exchange-holidays): free CSV of holidays, early closes and trading hours for nine stock exchanges (NYSE, LSE, TSX, Xetra, Euronext, Tokyo, HKEX, ASX, SIX), 2026-2028.
- [plainfoldhq/world-public-holidays](https://github.com/plainfoldhq/world-public-holidays): free CSV of public holidays for 20 countries and regions, 2026-2028, cross-checked against two independent implementations.
- [plainfoldhq/fx-settlement-holidays](https://github.com/plainfoldhq/fx-settlement-holidays): FX settlement holidays (USD, EUR/TARGET2, GBP, JPY, AUD, NZD) and T+2 spot value dates, 2026-2028, checked against QuantLib.
- All Plainfold data packs in one yearly plan: [All-Access](https://buy.polar.sh/polar_cl_xydfuofU72fdp6xSOHFtihAuniUFagYOwR9zf2M03Gl).

## License

Code: MIT. Data: CC0 1.0 (public domain). Made by Plainfold, with AI assistance. Not affiliated with any government agency. Questions: plainfoldhq@proton.me.
