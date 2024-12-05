import copy
import datetime
from typing import Any, Dict, List, Optional, Union

from lseg_analytics._client.client import Client
from lseg_analytics.common._resource_base import ResourceBase
from lseg_analytics.common._utils import convert_to_related
from lseg_analytics.exceptions import (
    LibraryException,
    ResourceNotFound,
    check_and_raise,
    check_exception_and_raise,
)
from lseg_analytics_basic_client.models import (
    AbsolutePositionWhen,
    CalculateDatesOutput,
    CalendarAsCollectionItem,
    CalendarDefinition,
    CalendarRelatedResource,
    CountPeriodsOutput,
    DateMovingConvention,
    DayCountBasis,
    Description,
    Direction,
    Duration,
    Frequency,
    FullDayDuration,
    HalfDayDuration,
    HolidayOutput,
    HolidayOutputNames,
    HolidayRule,
    IndexOrder,
    LagDaysRescheduleDescription,
    Location,
    Month,
    Observance,
    PeriodType,
    PeriodTypeOutput,
    RelativePositionWhen,
    RelativeRescheduleDescription,
    RelativeToRulePositionWhen,
    RescheduleDescription,
    RestDays,
    Time,
    ValidityPeriod,
    WeekDay,
    When,
)

from ._calendar import Calendar
from ._logger import logger

__all__ = [
    "AbsolutePositionWhen",
    "CalculateDatesOutput",
    "CalendarAsCollectionItem",
    "CalendarDefinition",
    "CalendarRelatedResource",
    "CountPeriodsOutput",
    "FullDayDuration",
    "HalfDayDuration",
    "HolidayOutput",
    "HolidayOutputNames",
    "HolidayRule",
    "LagDaysRescheduleDescription",
    "Observance",
    "PeriodTypeOutput",
    "RelativePositionWhen",
    "RelativeRescheduleDescription",
    "RelativeToRulePositionWhen",
    "RescheduleDescription",
    "RestDays",
    "When",
    "compute_dates",
    "count_periods",
    "delete",
    "generate_date_schedule",
    "generate_holidays",
    "load",
    "search",
]


def load(
    *,
    resource_id: Optional[str] = None,
    name: Optional[str] = None,
    space: Optional[str] = None,
):
    """
    Load a Calendar using its name and space

    Parameters
    ----------
    resource_id : str, optional
        The Calendar id.
        Required if name is not provided.
    name : str, optional
        The Calendar name.
        Required if resource_id is not provided. The name parameter must be specified when the object is first created. Thereafter it is optional.
    space : str, optional
        The space where the Calendar is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    Calendar
        The Calendar instance.

    Examples
    --------
    Load by Id.

    >>> load(resource_id="125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF")
    <Calendar space='my_personal_space' name='my_calendar' 125B1FCD‥>

    Load by name and space.

    >>> load(name="EMU", space="LSEG")
    <Calendar space='my_personal_space' name='my_calendar' 125B1FCD‥>

    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            logger.warn("resource_id argument received, name & space arguments are ignored")
        return _load_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Load Calendar {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"Calendar {name} not found in space={space!r}")
        raise ResourceNotFound(f"Resource Calendar not found by identifier name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    elif len(result) > 1:
        logger.warn(f"Found more than one result for name={name!r} and space={space!r}, returning the first one")
    return _load_by_id(result[0].id)


def delete(
    *,
    resource_id: Optional[str] = None,
    name: Optional[str] = None,
    space: Optional[str] = None,
):
    """
    Delete Calendar instance from the server.

    Parameters
    ----------
    resource_id : str, optional
        The Calendar resource ID.
        Required if name is not provided.
    name : str, optional
        The Calendar name.
        Required if resource_id is not provided.
    space : str, optional
        The space where the Calendar is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    ServiceErrorResponse, optional
        Error response, if applicable, otherwise None

    Examples
    --------
    Delete by Id.

    >>> delete(resource_id='125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF')
    True

    Delete by name and space.

    >>> delete(name="my_calendar", space="my_personal_space")
    True

    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            logger.warn("resource_id argument received, name & space arguments are ignored")
        return _delete_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Delete Calendar {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"Calendar {name} not found in space={space!r}")
        raise ResourceNotFound(f"Resource Calendar not found by identifier name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    return _delete_by_id(result[0].id)


def compute_dates(
    *,
    tenors: List[str],
    calendars: List[str],
    start_date: Optional[Union[str, datetime.date]] = None,
    date_moving_convention: Optional[Union[str, DateMovingConvention]] = None,
) -> List[CalculateDatesOutput]:
    """
    Computes dates for the calendar according to specified conditions

    Parameters
    ----------
    tenors : List[str]
        Tenors to be added to startDate to calculate the resulted dates.
        A tenor expresses a period of time using a specific syntax. For example "1D" for one day, "2W" for two weeks or "3W1M" for three weeks and a month.
        There are common tenors like ON, TN, SN, SW, 1W, 2W, 1M, 2M, etc.
    start_date : Union[str, datetime.date], optional
        The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01). Default is Today.
    date_moving_convention : Union[str, DateMovingConvention], optional
        The method to adjust dates to working days.
    calendars : List[str]
        An array of calendar reference strings for which the calculation should be done. Each string being composed of the space and name of a calendar. For example 'LSEG.UKG' is the string referencing the 'UKG' calendar stored in the 'LSEG' space.

    Returns
    --------
    List[CalculateDatesOutput]
        The result of the date calculation.

    Examples
    --------
    >>> compute_dates(
    >>>     calendars=['LSEG.UKG','LSEG.EUR'],
    >>>     tenors=["1M", "2M"],
    >>>     start_date=datetime.date(2023, 11, 1),
    >>>     date_moving_convention=DateMovingConvention.NEXT_BUSINESS_DAY
    >>> )
    [{'endDate': '2023-11-03', 'processingInformation': '<string>', 'tenor': '1M'},
     {'endDate': '2023-12-03', 'processingInformation': '<string>', 'tenor': '2M'}]

    """

    try:
        logger.info(f"Calling computeDates")

        calendars = convert_to_related(calendars)

        response = check_and_raise(
            Client().calendars_resource.compute_dates(
                tenors=tenors,
                start_date=start_date,
                date_moving_convention=date_moving_convention,
                calendars=calendars,
            )
        )

        output = response.data
        logger.info(f"Called computeDates")

        return output
    except Exception as err:
        logger.error(f"Error computeDates {err}")
        check_exception_and_raise(err)


def count_periods(
    *,
    start_date: Union[str, datetime.date],
    end_date: Union[str, datetime.date],
    day_count_basis: Optional[Union[str, DayCountBasis]] = None,
    period_type: Optional[Union[str, PeriodType]] = None,
    calendars: Optional[List[str]] = None,
) -> CountPeriodsOutput:
    """
    Counts the time periods that satisfy specified conditions. Note the use of date strings for convenience. Start and End Dates are included in the calculation.

    Parameters
    ----------
    start_date : Union[str, datetime.date]
        Start date for counting periods. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01).
    end_date : Union[str, datetime.date]
        End date for counting periods. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2024-01-01).
    day_count_basis : Union[str, DayCountBasis], optional
        The day count basis convention used to calculate the period between two dates.  Default is Actual/Actual.
        It is used when periodType is set to Year.
        Each convention defines the number of days between two dates and the year length in days (basis) for the period calculation.
    period_type : Union[str, PeriodType], optional
        The method of the period calculation. Default is WorkingDay.
    calendars : List[str], optional
        An array of calendar reference strings for which the calculation should be done. Each string being composed of the space and name of a calendar.
        For example 'LSEG.UKG' is the string referencing the 'UKG' calendar stored in the 'LSEG' space.
        The calendar parameter is optional only when periodType is "Day" or "Year".
        For a given day to be considered a working day, it must be a working day in all of the selected calendars.  If it is a non-working day in any of the calendars, it is a non-working day.

    Returns
    --------
    CountPeriodsOutput
        The result of the period calculation.

    Examples
    --------
    >>> count_periods(
    >>>     calendars=['LSEG.UKG'],
    >>>     start_date=datetime.date(2024, 5, 12),
    >>>     end_date=datetime.date(2024, 5, 29),
    >>>     day_count_basis=DayCountBasis.DCB_30_360,
    >>>     period_type=PeriodType.WORKING_DAY
    >>> )
    {'count': 13.0, 'periodType': 'WorkingDay', 'processingInformation': ''}

    """

    try:
        logger.info(f"Calling countPeriods")

        calendars = convert_to_related(calendars)

        response = check_and_raise(
            Client().calendars_resource.count_periods(
                start_date=start_date,
                end_date=end_date,
                day_count_basis=day_count_basis,
                period_type=period_type,
                calendars=calendars,
            )
        )

        output = response.data
        logger.info(f"Called countPeriods")

        return output
    except Exception as err:
        logger.error(f"Error countPeriods {err}")
        check_exception_and_raise(err)


def _delete_by_id(calendar_id: str) -> bool:
    """
    Delete resource.

    Parameters
    ----------
    calendar_id : str
        A sequence of textual characters.

    Returns
    --------
    bool


    Examples
    --------


    """

    try:
        logger.info(f"Deleting CalendarResource with id:  {calendar_id}")
        check_and_raise(Client().calendar_resource.delete(calendar_id=calendar_id))
        logger.info(f"Deleted CalendarResource with id:  {calendar_id}")

        return True
    except Exception as err:
        logger.error(f"Error deleting CalendarResource with id:  {calendar_id}")
        check_exception_and_raise(err)


def generate_date_schedule(
    *,
    frequency: Union[str, Frequency],
    calendars: List[str],
    start_date: Optional[Union[str, datetime.date]] = None,
    end_date: Optional[Union[str, datetime.date]] = None,
    calendar_day_of_month: Optional[int] = None,
    count: Optional[int] = None,
    day_of_week: Optional[Union[str, WeekDay]] = None,
) -> List[datetime.date]:
    """
    Generates a date schedule for the calendar according to specified conditions. Start and End Dates are included in the calculation.

    Parameters
    ----------
    frequency : Union[str, Frequency]
        The frequency of dates in the schedule which should be generated. Note that "Daily" refers to working days only.
    start_date : Union[str, datetime.date], optional
        The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01).
        The start date must be before the end date.
        Required if endDate is in the past.
    end_date : Union[str, datetime.date], optional
        The end date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2024-01-01).
        If startDate is not specified, endDate is used to define the list of dates from today's date to the end date.
        The end date must be after the start date.
        Required if count is not specified. Only one of endDate and count can be set at a time.
    calendar_day_of_month : int, optional
        The number of the day of the month. Required if frequency is Monthly; do not use otherwise. The minimum value is 1. The maximum value is 31.
    count : int, optional
        The number of dates to be generated, counting from the start date (or today's date if the start date is not set).
        It should not have a negative value.
        Required if endDate is not specified. Only one of endDate and count can be set at a time.
    day_of_week : Union[str, WeekDay], optional
        The day of the week. Required if frequency is Weekly or BiWeekly; do not use otherwise.
    calendars : List[str]
        An array of calendar reference strings for which the calculation should be done. Each string being composed of the space and name of a calendar. For example 'LSEG.UKG' is the string referencing the 'UKG' calendar stored in the 'LSEG' space.

    Returns
    --------
    List[datetime.date]
        A date on a calendar without a time zone, e.g. "April 10th"

    Examples
    --------
    >>> generate_date_schedule(
    >>>     calendars=['LSEG.UKG'],
    >>>     frequency=Frequency.DAILY,
    >>>     start_date=datetime.date(2023, 5, 5),
    >>>     end_date=datetime.date(2023, 11, 1),
    >>>     calendar_day_of_month=5,
    >>>     count=20,
    >>>     day_of_week=WeekDay.TUESDAY
    >>> )
    [datetime.date(2023, 5, 9),
     datetime.date(2023, 5, 16),
     datetime.date(2023, 5, 23),
     datetime.date(2023, 5, 30),
     datetime.date(2023, 6, 6),
     datetime.date(2023, 6, 13),
     datetime.date(2023, 6, 20),
     datetime.date(2023, 6, 27),
     datetime.date(2023, 7, 4),
     datetime.date(2023, 7, 11),
     datetime.date(2023, 7, 18),
     datetime.date(2023, 7, 25),
     datetime.date(2023, 8, 1),
     datetime.date(2023, 8, 8),
     datetime.date(2023, 8, 15),
     datetime.date(2023, 8, 22),
     datetime.date(2023, 8, 29),
     datetime.date(2023, 9, 5),
     datetime.date(2023, 9, 12),
     datetime.date(2023, 9, 19)]

    """

    try:
        logger.info(f"Calling generateDateSchedule")

        calendars = convert_to_related(calendars)

        response = check_and_raise(
            Client().calendars_resource.generate_date_schedule(
                frequency=frequency,
                start_date=start_date,
                end_date=end_date,
                calendar_day_of_month=calendar_day_of_month,
                count=count,
                day_of_week=day_of_week,
                calendars=calendars,
            )
        )

        output = response.data
        logger.info(f"Called generateDateSchedule")

        return output
    except Exception as err:
        logger.error(f"Error generateDateSchedule {err}")
        check_exception_and_raise(err)


def generate_holidays(
    *,
    end_date: Union[str, datetime.date],
    calendars: List[str],
    start_date: Optional[Union[str, datetime.date]] = None,
) -> List[HolidayOutput]:
    """
    Gets the holidays for the calendar within a date range. Start and End Dates are included in the calculation.

    Parameters
    ----------
    start_date : Union[str, datetime.date], optional
        The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01). Default is today.
    end_date : Union[str, datetime.date]
        The end date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2024-01-01).
    calendars : List[str]
        An array of calendar reference strings for which the calculation should be done. Each string being composed of the space and name of a calendar. For example 'LSEG.UKG' is the string referencing the 'UKG' calendar stored in the 'LSEG' space.

    Returns
    --------
    List[HolidayOutput]
        Dates and names of holidays for a requested calendar.

    Examples
    --------
    >>> response = generate_holidays(
    >>>     calendars=['LSEG.EMU','LSEG.UKG'],
    >>>     start_date=['2023-01-01'],
    >>>     end_date=['2023-01-31']
    >>> )
    >>> response[0]
    {'date': '2023-01-01', 'names': [{'name': "New Year's Day", 'calendars': [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'location': {'name': 'EMU', 'space': 'LSEG'}}, {'type': 'Calendar', 'id': '259B1FED-8MM3-4B1F-843F-5BA89EBE71AF', 'location': {'name': 'UKG', 'space': 'LSEG'}}], 'countries': ['', 'GBR']}], 'processingInformation': '<string>'}

    """

    try:
        logger.info(f"Calling generateHolidays")

        calendars = convert_to_related(calendars)

        response = check_and_raise(
            Client().calendars_resource.generate_holidays(start_date=start_date, end_date=end_date, calendars=calendars)
        )

        output = response.data
        logger.info(f"Called generateHolidays")

        return output
    except Exception as err:
        logger.error(f"Error generateHolidays {err}")
        check_exception_and_raise(err)


def _load_by_id(calendar_id: str) -> Calendar:
    """
    Read resource

    Parameters
    ----------
    calendar_id : str
        A sequence of textual characters.

    Returns
    --------
    Calendar


    Examples
    --------


    """

    try:
        logger.info(f"Opening CalendarResource with id:  {calendar_id}")

        response = check_and_raise(Client().calendar_resource.read(calendar_id=calendar_id))

        output = Calendar(response.data.definition, response.data.description)

        output._id = response.data.id

        output._location = response.data.location

        return output
    except Exception as err:
        logger.error(f"Error opening CalendarResource:  {err}")
        check_exception_and_raise(err)


def search(
    *,
    item_per_page: Optional[int] = None,
    names: Optional[List[str]] = None,
    spaces: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> List[CalendarAsCollectionItem]:
    """
    Search resources via combination of name, space and tags

    Parameters
    ----------
    item_per_page : int, optional
        The maximum number of items for each search request. The valid range is 1-500. If not provided, 50 will be used.
    names : List[str], optional
        The list of resource names to be searched. Exact match is applied for each name.
    spaces : List[str], optional
        The space where the resource is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.
    tags : List[str], optional
        The list of resource tags to be searched.

    Returns
    --------
    List[CalendarAsCollectionItem]
        An object describing the basic properties of a calendar.

    Examples
    --------
    Search all.

    >>> search()
    [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'description': {'tags': ['EU calendar'], 'summary': 'Calendar for Eurozone'}, 'location': {'name': 'EMU', 'space': 'LSEG'}}]

    Search by names and spaces.

    >>> search(names=["EMU"], spaces=["LSEG"])
    [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'description': {'tags': ['EU calendar'], 'summary': 'Calendar for Eurozone'}, 'location': {'name': 'EMU', 'space': 'LSEG'}}]

    Search by names.

    >>> search(names=["EMU"])
    [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'description': {'tags': ['EU calendar'], 'summary': 'Calendar for Eurozone'}, 'location': {'name': 'EMU', 'space': 'LSEG'}}]

    Search by spaces.

    >>> search(spaces=["LSEG"])
    [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'description': {'tags': ['EU calendar'], 'summary': 'Calendar for Eurozone'}, 'location': {'name': 'EMU', 'space': 'LSEG'}}]

    Search by tags.

    >>> search(tags=["EU calendar"])
    [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'description': {'tags': ['EU calendar'], 'summary': 'Calendar for Eurozone'}, 'location': {'name': 'EMU', 'space': 'LSEG'}}]

    """

    try:
        logger.info(f"Calling search")

        response = check_and_raise(
            Client().calendars_resource.list(item_per_page=item_per_page, names=names, spaces=spaces, tags=tags)
        )

        output = response.data
        logger.info(f"Called search")

        return output
    except Exception as err:
        logger.error(f"Error search {err}")
        check_exception_and_raise(err)
