import numpy as np

from datetime import datetime, timedelta
import pytz
eastern = pytz.timezone('US/Eastern')
import pandas_market_calendars as mcal


def get_prev_market_day(dt):
    """
    Get previous market day, accounting for weekends and market holidays.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime.

    Returns
    -------
    datetime.datetime
        Previous market day datetime.
    """

    ydt = eastern.normalize(dt - timedelta(1))  # yesterday

    # check if previous day the weekend
    if ydt.weekday() == 5: ydt = eastern.normalize(ydt - timedelta(1))
    elif ydt.weekday() == 6: ydt = eastern.normalize(ydt - timedelta(2))

    # check for holiday
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays
    if str(ydt.date()) in np.datetime_as_string(nyse_holidays):
        ydt = eastern.normalize(ydt - timedelta(1))

    # check for weekend again
    if ydt.weekday() == 6: ydt = eastern.normalize(ydt - timedelta(2))

    return ydt


def get_prev_market_days(dt, n):
    """
    Get the previous n market days.

    Parameters
    ----------
    dt : datetime.datetime
        Date for which to get previous market days.
    n : int
        Number of previous market days to get.

    Returns
    -------
    list of datetime.datetime
        List of previous market days, sorted chronologically.
    """

    prev_days = []
    while len(prev_days) < n:
        dt = get_prev_market_day(dt)
        prev_days.append(dt)
    return sorted(prev_days)


def get_next_market_day(dt):
    """
    Get next market day, accounting for weekends and market holidays.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime.

    Returns
    -------
    datetime.datetime
        Next market day datetime.
    """

    tdt = eastern.normalize(dt + timedelta(1))  # tomorrow

    # check if next day the weekend
    if tdt.weekday() == 5: tdt = eastern.normalize(tdt + timedelta(2))
    elif tdt.weekday() == 6: tdt = eastern.normalize(tdt + timedelta(1))

    # check for holiday
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays
    if str(tdt.date()) in np.datetime_as_string(nyse_holidays):
        tdt = eastern.normalize(tdt + timedelta(1))

    # check for weekend again
    if tdt.weekday() == 5: tdt = eastern.normalize(tdt + timedelta(2))

    return tdt


def get_quarter_start(dt):
    """
    Get start date of the current quarter.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime

    Returns
    -------
    datetime.datetime
        Datetime of last quarter end.
    """

    # get current month and year
    month = dt.month
    year = dt.year

    # calculate first day of current quarter
    quarter_start = datetime(year, ((month-1) // 3) * 3 + 1, 1).astimezone(eastern)
    return quarter_start


def get_last_quarter_end(dt):
    """
    Get date of last quarter end.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime

    Returns
    -------
    datetime.datetime
        Datetime of last quarter end.
    """

    # calculate first day of current quarter
    quarter_start = get_quarter_start(dt)

    # calculate last day of previous quarter
    last_quarter_end = eastern.normalize(quarter_start - timedelta(1))

    return last_quarter_end


def is_not_market_day(dt):
    """
    Check if a given date is a market holiday or weekend.

    Parameters
    ----------
    dt : datetime.datetime
        Date to check.

    Returns
    -------
    bool
        True if date is not a market day, False otherwise.
    """
    # check for weekend
    if dt.weekday() in [5, 6]:
        return True
    
    # check for holiday
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays
    if dt.strftime("%Y-%m-%d") in np.datetime_as_string(nyse_holidays):
        return True

    return False


def market_dates(start_date, end_date):
    """
    Get market dates between start and end dates.

    Parameters
    ----------
    start_date : datetime.datetime or str
        Start date. If str, must be in YYYY-MM-DD format.
    end_date : datetime.datetime or str
        End date. Not included in the output.
        If str, must be in YYYY-MM-DD format.

    Returns
    -------
    list of datetime.datetime
        List of market dates between start and end dates.
    """
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays

    # if input dates are strings, convert to datetime
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    while start_date < end_date:
        if (not start_date.date() in nyse_holidays) and (start_date.weekday() < 5):
            dates.append(start_date)
        start_date += timedelta(days=1)

    return dates
