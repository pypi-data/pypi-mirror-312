from typing import List, Union

from lseg_analytics.market_data.fx_forward_curves import FxForwardCurvePoint
from lseg_analytics.reference_data.calendars import HolidayOutput

__all__ = ["to_rows"]


def _plain_curve_point(point: FxForwardCurvePoint):
    return {
        "tenor": point.tenor,
        "start_date": point.start_date,
        "end_date": point.end_date,
        "swap_point.bid": point.swap_point.bid,
        "swap_point.ask": point.swap_point.ask,
        "swap_point.mid": point.swap_point.mid,
        "outright.bid": point.outright.bid,
        "outright.ask": point.outright.ask,
        "outright.mid": point.outright.mid,
    }


def _plain_holiday_output(output: HolidayOutput):
    for oname in output.names:
        yield {
            "date": output.date,
            "name": oname.name,
            "calendars": [f"{calendar.location.space}.{calendar.location.name}" for calendar in oname.calendars],
            "countries": oname.countries,
        }


def to_rows(items: List[Union[FxForwardCurvePoint]]) -> List[dict]:
    """Convert list of objects to list of dicts, that can be passed to a DataFrame constructor"""

    if isinstance(items, list):
        if not items:
            return []
        if isinstance(items[0], FxForwardCurvePoint):  # TODO: What if not all items in the list are FxForwardCurvePoint
            return [_plain_curve_point(point) for point in items]
        elif isinstance(items[0], HolidayOutput):
            result = []
            for item in items:
                result.extend(_plain_holiday_output(item))
            return result
    raise ValueError("Argument is not supported")
