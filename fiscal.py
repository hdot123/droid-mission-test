"""Fiscal year, quarter, label, and start-date helpers (standard library only)."""

from datetime import date

__all__ = ["fiscal_year", "fiscal_quarter", "fiscal_label", "fiscal_start"]


def _validate(d, start_month):
    if not isinstance(d, date):
        raise TypeError("d must be a datetime.date instance")
    if not isinstance(start_month, int) or isinstance(start_month, bool):
        raise TypeError("start_month must be an int")
    if not 1 <= start_month <= 12:
        raise ValueError("start_month must be in 1-12")


def _fiscal_start_year(d, start_month):
    """Year in which the fiscal year containing d begins."""
    return d.year if d.month >= start_month else d.year - 1


def _end_year(d, start_month):
    """Fiscal year is named by its end year: start year + 1, except when the
    fiscal year ends on Dec 31 of the fiscal start year (start_month == 1),
    where the end year equals the fiscal start year."""
    start_year = _fiscal_start_year(d, start_month)
    if start_month == 1:
        return start_year
    return start_year + 1


def fiscal_year(d, start_month):
    # type: (date, int) -> int
    """Return the fiscal year (named by end year) containing date d."""
    _validate(d, start_month)
    return _end_year(d, start_month)


def fiscal_quarter(d, start_month):
    # type: (date, int) -> int
    """Return the fiscal quarter (1-4) of date d within its fiscal year."""
    _validate(d, start_month)
    offset = (d.month - start_month) % 12
    return offset // 3 + 1


def fiscal_label(d, start_month):
    # type: (date, int) -> str
    """Return a label like ``FY2027-Q1`` for date d."""
    return "FY{}-Q{}".format(fiscal_year(d, start_month), fiscal_quarter(d, start_month))


def fiscal_start(d, start_month):
    # type: (date, int) -> date
    """Return the first date (start_month 1) of the fiscal year containing d."""
    _validate(d, start_month)
    return date(_fiscal_start_year(d, start_month), start_month, 1)
