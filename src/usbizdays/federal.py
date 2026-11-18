"""US federal holidays per 5 U.S.C. 6103 with observed dates. Part of usbizdays. MIT license."""
from datetime import date, timedelta


def nth_weekday(year, month, weekday, n):
    """n-th (1-based) given weekday (Mon=0) of a month."""
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def last_weekday(year, month, weekday):
    d = date(year + (month == 12), month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def observed(d):
    """Saturday -> preceding Friday, Sunday -> following Monday.
    Jan 1 on Saturday therefore gives Dec 31 of the prior year (OPM practice)."""
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def holidays_for_year(y):
    """Return list of (name, slug, actual_date) for year y."""
    h = [("New Year's Day", "new-years-day", date(y, 1, 1))]
    if y >= 1986:  # first observed Jan 1986
        h.append(("Birthday of Martin Luther King, Jr.", "martin-luther-king-jr-day",
                  nth_weekday(y, 1, 0, 3)))
    h.append(("Washington's Birthday", "washingtons-birthday", nth_weekday(y, 2, 0, 3)))
    h.append(("Memorial Day", "memorial-day", last_weekday(y, 5, 0)))
    if y >= 2021:
        h.append(("Juneteenth National Independence Day", "juneteenth", date(y, 6, 19)))
    h.append(("Independence Day", "independence-day", date(y, 7, 4)))
    h.append(("Labor Day", "labor-day", nth_weekday(y, 9, 0, 1)))
    h.append(("Columbus Day", "columbus-day", nth_weekday(y, 10, 0, 2)))
    # Veterans Day: 4th Monday of October 1971-1977, Nov 11 from 1978.
    if y <= 1977:
        h.append(("Veterans Day", "veterans-day", nth_weekday(y, 10, 0, 4)))
    else:
        h.append(("Veterans Day", "veterans-day", date(y, 11, 11)))
    h.append(("Thanksgiving Day", "thanksgiving-day", nth_weekday(y, 11, 3, 4)))
    h.append(("Christmas Day", "christmas-day", date(y, 12, 25)))
    return h
