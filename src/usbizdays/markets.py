#!/usr/bin/env python3
"""NYSE trading calendar and Federal Reserve Bank holidays, 2000-2050.

Python 3 standard library only. MIT license.
NYSE rules (NYSE Rule 51 practice): New Year's Day, MLK Day, Washington's
Birthday, Good Friday, Memorial Day, Juneteenth (from 2022), Independence Day,
Labor Day, Thanksgiving, Christmas. Saturday holiday -> closed the Friday before,
EXCEPT New Year's Day (no Friday closure at year end); Sunday -> Monday.
Regular 1:00 pm early closes: July 3 when July 4 is Tue-Fri; the day after
Thanksgiving; December 24 when December 25 is Tue-Fri. Past unscheduled
closures and changed early closes 2000-2025 are listed below.

Federal Reserve Banks: the federal holidays of 5 U.S.C. 6103 (Juneteenth from
2022). Saturday holiday -> NOT moved (banks open the Friday before); Sunday
holiday -> the following Monday.
"""
from datetime import date, timedelta

from . import federal as g

YEARS = range(2000, 2051)

NYSE_SPECIAL_CLOSURES = {
    date(2001, 9, 11): "Closed following the September 11 attacks",
    date(2001, 9, 12): "Closed following the September 11 attacks",
    date(2001, 9, 13): "Closed following the September 11 attacks",
    date(2001, 9, 14): "Closed following the September 11 attacks",
    date(2004, 6, 11): "National Day of Mourning for former President Ronald Reagan",
    date(2007, 1, 2): "National Day of Mourning for former President Gerald R. Ford",
    date(2012, 10, 29): "Hurricane Sandy",
    date(2012, 10, 30): "Hurricane Sandy",
    date(2018, 12, 5): "National Day of Mourning for former President George H. W. Bush",
    date(2025, 1, 9): "National Day of Mourning for former President Jimmy Carter",
}
# Early closes that differ from the regular rule (added; regular July 3 skipped in 2002).
NYSE_SPECIAL_EARLY = {
    date(2002, 7, 5): "Day after Independence Day",
    date(2003, 12, 26): "Friday after Christmas",
}
NYSE_SKIP_JUL3 = {2002}


def easter(y):
    """Gregorian Easter Sunday (anonymous Gregorian algorithm)."""
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    gg = (b - f + 1) // 3
    h = (19 * a + b - d - gg + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(y, month, day)


def nyse_holidays(y):
    """{date: name} of NYSE full-day closures in calendar year y (rules + specials)."""
    out = {}
    raw = [("New Year's Day", date(y, 1, 1))]
    if y >= 1998:
        raw.append(("Martin Luther King Jr. Day", g.nth_weekday(y, 1, 0, 3)))
    raw += [("Washington's Birthday", g.nth_weekday(y, 2, 0, 3)),
            ("Good Friday", easter(y) - timedelta(days=2)),
            ("Memorial Day", g.last_weekday(y, 5, 0))]
    if y >= 2022:
        raw.append(("Juneteenth National Independence Day", date(y, 6, 19)))
    raw += [("Independence Day", date(y, 7, 4)),
            ("Labor Day", g.nth_weekday(y, 9, 0, 1)),
            ("Thanksgiving Day", g.nth_weekday(y, 11, 3, 4)),
            ("Christmas Day", date(y, 12, 25))]
    for name, d in raw:
        if d.weekday() == 5:
            if name == "New Year's Day":
                continue  # not observed on Dec 31
            out[d - timedelta(days=1)] = name + " (observed)"
        elif d.weekday() == 6:
            out[d + timedelta(days=1)] = name + " (observed)"
        else:
            out[d] = name
    for d, name in NYSE_SPECIAL_CLOSURES.items():
        if d.year == y:
            out[d] = name
    return out


def nyse_early_closes(y):
    """{date: reason} of 1:00 pm early closes in year y."""
    out = {}
    j4 = date(y, 7, 4)
    if 1 <= j4.weekday() <= 4 and y not in NYSE_SKIP_JUL3:
        out[date(y, 7, 3)] = "Day before Independence Day"
    out[g.nth_weekday(y, 11, 3, 4) + timedelta(days=1)] = "Day after Thanksgiving Day"
    c = date(y, 12, 25)
    if 1 <= c.weekday() <= 4:
        out[date(y, 12, 24)] = "Christmas Eve"
    for d, name in NYSE_SPECIAL_EARLY.items():
        if d.year == y:
            out[d] = name
    closed = nyse_holidays(y)
    return {d: r for d, r in out.items() if d not in closed}


def fed_holidays(y):
    """{date: name} of Federal Reserve Bank holidays observed in year y."""
    out = {}
    for name, _slug, d in g.holidays_for_year(y):
        if name.startswith("Juneteenth") and y < 2022:
            continue
        if d.weekday() == 5:
            continue  # Saturday: banks open the Friday before
        if d.weekday() == 6:
            out[d + timedelta(days=1)] = name + " (observed)"
        else:
            out[d] = name
    return out


def daily_rows():
    nyse, early, fed = {}, {}, {}
    for y in range(YEARS[0] - 1, YEARS[-1] + 2):
        nyse.update(nyse_holidays(y))
        early.update(nyse_early_closes(y))
        fed.update(fed_holidays(y))

    def trading(d):
        return d.weekday() < 5 and d not in nyse

    def step(d, k):
        d += timedelta(days=k)
        while not trading(d):
            d += timedelta(days=k)
        return d

    rows, d, end = [], date(YEARS[0], 1, 1), date(YEARS[-1], 12, 31)
    while d <= end:
        t = trading(d)
        rows.append({
            "date": d.isoformat(),
            "weekday": d.strftime("%A"),
            "is_nyse_trading_day": int(t),
            "nyse_closed_reason": nyse.get(d, ""),
            "is_nyse_early_close": int(t and d in early),
            "nyse_close_time_et": ("13:00" if d in early else "16:00") if t else "",
            "previous_nyse_trading_day": step(d, -1).isoformat(),
            "next_nyse_trading_day": step(d, 1).isoformat(),
            "is_fed_business_day": int(d.weekday() < 5 and d not in fed),
            "fed_holiday": fed.get(d, ""),
        })
        d += timedelta(days=1)
    return rows, nyse, early, fed


