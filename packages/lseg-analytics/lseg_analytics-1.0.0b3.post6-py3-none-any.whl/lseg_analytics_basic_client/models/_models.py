# coding=utf-8
# pylint: disable=too-many-lines


import datetime
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
    overload,
)

from .. import _model_base
from .._model_base import rest_discriminator, rest_field
from ._enums import (
    DateType,
    DurationType,
    FxForwardCurveConstituentType,
    PositionType,
    RescheduleType,
    ResourceType,
)

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import (
        MutableMapping,  # type: ignore  # pylint: disable=ungrouped-imports
    )

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from .. import models as _models
JSON = MutableMapping[str, Any]  # pylint: disable=unsubscriptable-object


class When(_model_base.Model):
    """An object to determine a regular annual holiday rule for the calendar.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    AbsolutePositionWhen, RelativePositionWhen, RelativeToRulePositionWhen


    :ivar position_type: The type of regular annual holiday rule. Possible values are:
     AbsolutePositionWhen (for fixed holidays), RelativePositionWhen (for holidays that fall on a
     particular day of the week) or RelativeToRulePositionWhen (for holidays that are set by
     reference to another date). Required. Known values are: "AbsolutePositionWhen",
     "RelativePositionWhen", and "RelativeToRulePositionWhen".
    :vartype position_type: str or ~analyticsapi.models.PositionType
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    position_type: str = rest_discriminator(name="positionType")
    """The type of regular annual holiday rule. Possible values are: AbsolutePositionWhen (for fixed
     holidays), RelativePositionWhen (for holidays that fall on a particular day of the week) or
     RelativeToRulePositionWhen (for holidays that are set by reference to another date). Required.
     Known values are: \"AbsolutePositionWhen\", \"RelativePositionWhen\", and
     \"RelativeToRulePositionWhen\"."""

    @overload
    def __init__(
        self,
        position_type: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["position_type"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class AbsolutePositionWhen(When, discriminator="AbsolutePositionWhen"):
    """An absolute position annual holiday rule. For example, New Year holiday on 1st Jan.

    Attributes
    ----------
    position_type : str or ~analyticsapi.models.ABSOLUTE_POSITION_WHEN
        The type of regular annual holiday rule. Only AbsolutePositionWhen
        value applies. Required. The holiday is on a fixed date. For example,
        New Year holiday on January 1.
    day_of_month : int
        The number of the day of the month. The minimum value is 0 (a special
        case indicating western Easter). The maximum value is 31. Required.
    month : str or ~analyticsapi.models.Month
        The month of the year, written in full (e.g. January). Known values
        are: "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", and "December".
    observance : list[~analyticsapi.models.Observance]
        An array of objects to determine how the holiday is rescheduled if it
        falls on a rest day.
    """

    position_type: Literal[PositionType.ABSOLUTE_POSITION_WHEN] = rest_discriminator(name="positionType")  # type: ignore
    """The type of regular annual holiday rule. Only AbsolutePositionWhen value applies. Required. The
     holiday is on a fixed date. For example, New Year holiday on January 1."""
    day_of_month: int = rest_field(name="dayOfMonth")
    """The number of the day of the month. The minimum value is 0 (a special case indicating western
     Easter). The maximum value is 31. Required."""
    month: Optional[Union[str, "_models.Month"]] = rest_field()
    """The month of the year, written in full (e.g. January). Known values are: \"January\",
     \"February\", \"March\", \"April\", \"May\", \"June\", \"July\", \"August\", \"September\",
     \"October\", \"November\", and \"December\"."""
    observance: Optional[List["_models.Observance"]] = rest_field()
    """An array of objects to determine how the holiday is rescheduled if it falls on a rest day."""

    @overload
    def __init__(
        self,
        *,
        day_of_month: int,
        month: Optional[Union[str, "_models.Month"]] = None,
        observance: Optional[List["_models.Observance"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, position_type=PositionType.ABSOLUTE_POSITION_WHEN, **kwargs)
        if self.observance is None:
            self.observance = list()


class Date(_model_base.Model):
    """Date.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    AdjustableDate, RelativeAdjustableDate

    Attributes
    ----------
    date_type : str or ~analyticsapi.models.DateType
        Required. Known values are: "AdjustableDate" and
        "RelativeAdjustableDate".
    date_moving_convention : str or ~analyticsapi.models.DateMovingConvention
        The method to adjust dates to working days. The possible values are:
        ModifiedFollowing: dates are adjusted to the next business day
        convention unless it goes into the next month. In such case, the
        previous business day convention is used, NextBusinessDay: dates are
        moved to the following working day, PreviousBusinessDay: dates are
        moved to the preceding working day, NoMoving: dates are not adjusted,
        EveryThirdWednesday: dates are moved to the third Wednesday of the
        month, or to the next working day if the third Wednesday is not a
        working day, BbswModifiedFollowing: dates are adjusted to the next
        business day convention unless it goes into the next month, or crosses
        mid-month (15th). In such case, the previous business day convention is
        used. Default is ModifiedFollowing. Known values are:
        "ModifiedFollowing", "NextBusinessDay", "PreviousBusinessDay",
        "NoMoving", "EveryThirdWednesday", and "BbswModifiedFollowing".
    calendars : list[~analyticsapi.models.CalendarRelatedResource]
        An array of calendars that should be used for the date adjustment.
        Typically the calendars are derived based on the instruments currency
        or crossCurrency code.
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    date_type: str = rest_discriminator(name="dateType")
    """Required. Known values are: \"AdjustableDate\" and \"RelativeAdjustableDate\"."""
    date_moving_convention: Optional[Union[str, "_models.DateMovingConvention"]] = rest_field(
        name="dateMovingConvention"
    )
    """The method to adjust dates to working days. The possible values are: ModifiedFollowing: dates
     are adjusted to the next business day convention unless it goes into the next month. In such
     case, the previous business day convention is used, NextBusinessDay: dates are moved to the
     following working day, PreviousBusinessDay: dates are moved to the preceding working day,
     NoMoving: dates are not adjusted, EveryThirdWednesday: dates are moved to the third Wednesday
     of the month, or to the next working day if the third Wednesday is not a working day,
     BbswModifiedFollowing: dates are adjusted to the next business day convention unless it goes
     into the next month, or crosses mid-month (15th). In such case, the previous business day
     convention is used. Default is ModifiedFollowing. Known values are: \"ModifiedFollowing\",
     \"NextBusinessDay\", \"PreviousBusinessDay\", \"NoMoving\", \"EveryThirdWednesday\", and
     \"BbswModifiedFollowing\"."""
    calendars: Optional[List["_models.CalendarRelatedResource"]] = rest_field()
    """An array of calendars that should be used for the date adjustment. Typically the calendars are
     derived based on the instruments currency or crossCurrency code."""

    @overload
    def __init__(
        self,
        *,
        date_type: str,
        date_moving_convention: Optional[Union[str, "_models.DateMovingConvention"]] = None,
        calendars: Optional[List["_models.CalendarRelatedResource"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.calendars is None:
            self.calendars = list()


class AdjustableDate(Date, discriminator="AdjustableDate"):
    """AdjustableDate.

    Attributes
    ----------
    date_moving_convention : str or ~analyticsapi.models.DateMovingConvention
        The method to adjust dates to working days. The possible values are:
        ModifiedFollowing: dates are adjusted to the next business day
        convention unless it goes into the next month. In such case, the
        previous business day convention is used, NextBusinessDay: dates are
        moved to the following working day, PreviousBusinessDay: dates are
        moved to the preceding working day, NoMoving: dates are not adjusted,
        EveryThirdWednesday: dates are moved to the third Wednesday of the
        month, or to the next working day if the third Wednesday is not a
        working day, BbswModifiedFollowing: dates are adjusted to the next
        business day convention unless it goes into the next month, or crosses
        mid-month (15th). In such case, the previous business day convention is
        used. Default is ModifiedFollowing. Known values are:
        "ModifiedFollowing", "NextBusinessDay", "PreviousBusinessDay",
        "NoMoving", "EveryThirdWednesday", and "BbswModifiedFollowing".
    calendars : list[~analyticsapi.models.CalendarRelatedResource]
        An array of calendars that should be used for the date adjustment.
        Typically the calendars are derived based on the instruments currency
        or crossCurrency code.
    date_type : str or ~analyticsapi.models.ADJUSTABLE_DATE
        Required.
    date : ~datetime.date
        The date that will be adjusted based on the dateMovingConvention.The
        value is expressed in ISO 8601 format: YYYY-MM-DD (e.g. 2021-01-01).
        Required.
    """

    date_type: Literal[DateType.ADJUSTABLE_DATE] = rest_discriminator(name="dateType")  # type: ignore
    """Required."""
    date: datetime.date = rest_field()
    """The date that will be adjusted based on the dateMovingConvention.The value is expressed in ISO
     8601 format: YYYY-MM-DD (e.g. 2021-01-01). Required."""

    @overload
    def __init__(
        self,
        *,
        date: datetime.date,
        date_moving_convention: Optional[Union[str, "_models.DateMovingConvention"]] = None,
        calendars: Optional[List["_models.CalendarRelatedResource"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, date_type=DateType.ADJUSTABLE_DATE, **kwargs)
        if self.calendars is None:
            self.calendars = list()


class AdjustedDate(_model_base.Model):
    """AdjustedDate.

    Attributes
    ----------
    un_adjusted : ~datetime.date
        The unadjusted date. The value is expressed in ISO 8601 format: YYYY-
        MM-DD (e.g. 2021-01-01). Required.
    adjusted : ~datetime.date
        The date that has been adjusted based on the dateMovingConvention. The
        value is expressed in ISO 8601 format: YYYY-MM-DD (e.g. 2021-01-01).
        Required.
    date_moving_convention : str or ~analyticsapi.models.DateMovingConvention
        Required. Known values are: "ModifiedFollowing", "NextBusinessDay",
        "PreviousBusinessDay", "NoMoving", "EveryThirdWednesday", and
        "BbswModifiedFollowing".
    reference_date : str or ~analyticsapi.models.ReferenceDate
        The date which has been used as a reference date for the provided
        tenor. Possible values are: StartDate, ValuationDate, SpotDate. Known
        values are: "SpotDate", "StartDate", and "ValuationDate".
    date : ~datetime.date
        The date provided in the request. The value is expressed in ISO 8601
        format: YYYY-MM-DD (e.g. 2021-01-01).
    tenor : str
        A tenor (relatvie date) expressed as a code indicating the period
        between referenceDate(default=startDate) to endDate of the instrument
        (e.g., '6M', '1Y').
    processing_information : str
        The error message for the calculation in case of a non-blocking error.
    """

    un_adjusted: datetime.date = rest_field(name="unAdjusted")
    """The unadjusted date. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g. 2021-01-01).
     Required."""
    adjusted: datetime.date = rest_field()
    """The date that has been adjusted based on the dateMovingConvention. The value is expressed in
     ISO 8601 format: YYYY-MM-DD (e.g. 2021-01-01). Required."""
    date_moving_convention: Union[str, "_models.DateMovingConvention"] = rest_field(name="dateMovingConvention")
    """Required. Known values are: \"ModifiedFollowing\", \"NextBusinessDay\",
     \"PreviousBusinessDay\", \"NoMoving\", \"EveryThirdWednesday\", and \"BbswModifiedFollowing\"."""
    reference_date: Optional[Union[str, "_models.ReferenceDate"]] = rest_field(name="referenceDate")
    """The date which has been used as a reference date for the provided tenor. Possible values are:
     StartDate, ValuationDate, SpotDate. Known values are: \"SpotDate\", \"StartDate\", and
     \"ValuationDate\"."""
    date: Optional[datetime.date] = rest_field()
    """The date provided in the request. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g.
     2021-01-01)."""
    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code indicating the period between
     referenceDate(default=startDate) to endDate of the instrument (e.g., '6M', '1Y')."""
    processing_information: Optional[str] = rest_field(name="processingInformation")
    """The error message for the calculation in case of a non-blocking error."""

    @overload
    def __init__(
        self,
        *,
        un_adjusted: datetime.date,
        adjusted: datetime.date,
        date_moving_convention: Union[str, "_models.DateMovingConvention"],
        reference_date: Optional[Union[str, "_models.ReferenceDate"]] = None,
        date: Optional[datetime.date] = None,
        tenor: Optional[str] = None,
        processing_information: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class BidAskMidSimpleValues(_model_base.Model):
    """An object that contains the bid, ask and mid quotes for the instrument.

    Attributes
    ----------
    bid : float
        The bid value.
    ask : float
        The ask value.
    mid : float
        The mid value.
    """

    bid: Optional[float] = rest_field()
    """The bid value."""
    ask: Optional[float] = rest_field()
    """The ask value."""
    mid: Optional[float] = rest_field()
    """The mid value."""

    @overload
    def __init__(
        self,
        *,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        mid: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class BidAskSimpleValues(_model_base.Model):
    """An object that contains the bid and ask quotes for the instrument.

    Attributes
    ----------
    bid : float
        The bid quote.
    ask : float
        The ask quote.
    """

    bid: Optional[float] = rest_field()
    """The bid quote."""
    ask: Optional[float] = rest_field()
    """The ask quote."""

    @overload
    def __init__(
        self,
        *,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class BidAskValues(_model_base.Model):
    """An object that contains the bid and ask quotes for the instrument.

    Attributes
    ----------
    bid : ~analyticsapi.models.FieldValue
        An object that contains the bid quote for the instrument.
    ask : ~analyticsapi.models.FieldValue
        An object that contains the ask quote for the instrument.
    """

    bid: Optional["_models.FieldValue"] = rest_field()
    """An object that contains the bid quote for the instrument."""
    ask: Optional["_models.FieldValue"] = rest_field()
    """An object that contains the ask quote for the instrument."""

    @overload
    def __init__(
        self,
        *,
        bid: Optional["_models.FieldValue"] = None,
        ask: Optional["_models.FieldValue"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class BuildDirectFromDepositsResponse(_model_base.Model):
    """BuildDirectFromDepositsResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.FxForwardCurveAsTransient
        Required.
    """

    data: "_models.FxForwardCurveAsTransient" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        data: "_models.FxForwardCurveAsTransient",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["data"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class CalculateDatesOutput(_model_base.Model):
    """The result of the date calculation.

    Attributes
    ----------
    tenor : str
        The code indicating the tenor added to startDate to calculate the
        resulted date (e.g., 1Y).
    end_date : ~datetime.date
        The date produced by the calculation. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., 2024-01-01).
    processing_information : str
        The error message for the calculation in case of a non-blocking error.
    """

    tenor: Optional[str] = rest_field()
    """The code indicating the tenor added to startDate to calculate the resulted date (e.g., 1Y)."""
    end_date: Optional[datetime.date] = rest_field(name="endDate")
    """The date produced by the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., 2024-01-01)."""
    processing_information: Optional[str] = rest_field(name="processingInformation")
    """The error message for the calculation in case of a non-blocking error."""

    @overload
    def __init__(
        self,
        *,
        tenor: Optional[str] = None,
        end_date: Optional[datetime.date] = None,
        processing_information: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CalendarAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of a calendar.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CALENDAR
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.CALENDAR]] = rest_field(visibility=["read"], default=ResourceType.CALENDAR)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CalendarCollectionLinks(_model_base.Model):
    """CalendarCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    generate_holidays : ~analyticsapi.models.Link
        Required.
    compute_dates : ~analyticsapi.models.Link
        Required.
    generate_date_schedule : ~analyticsapi.models.Link
        Required.
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()
    generate_holidays: "_models.Link" = rest_field(name="generateHolidays")
    """Required."""
    compute_dates: "_models.Link" = rest_field(name="computeDates")
    """Required."""
    generate_date_schedule: "_models.Link" = rest_field(name="generateDateSchedule")
    """Required."""

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        generate_holidays: "_models.Link",
        compute_dates: "_models.Link",
        generate_date_schedule: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CalendarCollectionResponse(_model_base.Model):
    """CalendarCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.CalendarAsCollectionItem]
        Required.
    links : ~analyticsapi.models.CalendarCollectionLinks
    """

    data: List["_models.CalendarAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.CalendarCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.CalendarAsCollectionItem"],
        links: Optional["_models.CalendarCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class CalendarDefinition(_model_base.Model):
    """Calendar definition object that contains rest days, first day of week, holiday rules and
    holiday exception rules.

    Attributes
    ----------
    rest_days : list[~analyticsapi.models.RestDays]
        An array of objects that define the rest days for the calendar.
    first_day_of_week : str or ~analyticsapi.models.WeekDay
        The first day of the week set for the calendar. Known values are:
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", and
        "Sunday".
    holiday_rules : list[~analyticsapi.models.HolidayRule]
        An array of objects that define the calendar's regular holiday rules
        and half holiday rules.
    holiday_exception_rules : list[~analyticsapi.models.HolidayRule]
        An array of objects that define the calendar's exception day rules for
        the calendar.
    """

    rest_days: Optional[List["_models.RestDays"]] = rest_field(name="restDays")
    """An array of objects that define the rest days for the calendar."""
    first_day_of_week: Optional[Union[str, "_models.WeekDay"]] = rest_field(name="firstDayOfWeek")
    """The first day of the week set for the calendar. Known values are: \"Monday\", \"Tuesday\",
     \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", and \"Sunday\"."""
    holiday_rules: Optional[List["_models.HolidayRule"]] = rest_field(name="holidayRules")
    """An array of objects that define the calendar's regular holiday rules and half holiday rules."""
    holiday_exception_rules: Optional[List["_models.HolidayRule"]] = rest_field(name="holidayExceptionRules")
    """An array of objects that define the calendar's exception day rules for the calendar."""

    @overload
    def __init__(
        self,
        *,
        rest_days: Optional[List["_models.RestDays"]] = None,
        first_day_of_week: Optional[Union[str, "_models.WeekDay"]] = None,
        holiday_rules: Optional[List["_models.HolidayRule"]] = None,
        holiday_exception_rules: Optional[List["_models.HolidayRule"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.rest_days is None:
            self.rest_days = list()
        if self.holiday_rules is None:
            self.holiday_rules = list()
        if self.holiday_exception_rules is None:
            self.holiday_exception_rules = list()


class CalendarRelatedResource(_model_base.Model):
    """Object identifying a calendar resource by either uuid or location (space and name).

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CALENDAR
        The type of the resource.
    id : str
        The unique id of the resource.
    location : ~analyticsapi.models.Location
        An object to define the location of the resource (space and name).
    """

    type: Optional[Literal[ResourceType.CALENDAR]] = rest_field(visibility=["read"], default=ResourceType.CALENDAR)
    """The type of the resource."""
    id: Optional[str] = rest_field()
    """The unique id of the resource."""
    location: Optional["_models.Location"] = rest_field()
    """An object to define the location of the resource (space and name)."""

    @overload
    def __init__(
        self,
        *,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        location: Optional["_models.Location"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CalendarResource(_model_base.Model):
    """Calendar resource including calendar definition and description.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CALENDAR
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Calendar description.
    definition : ~analyticsapi.models.CalendarDefinition
        Calendar definition. Required.
    """

    type: Optional[Literal[ResourceType.CALENDAR]] = rest_field(visibility=["read"], default=ResourceType.CALENDAR)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Calendar description."""
    definition: "_models.CalendarDefinition" = rest_field()
    """Calendar definition. Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.CalendarDefinition",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CalendarResponse(_model_base.Model):
    """CalendarResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.CalendarResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.CalendarResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.CalendarResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CollectionLinks(_model_base.Model):
    """CollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class ComputeDatesResponse(_model_base.Model):
    """ComputeDatesResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.CalculateDatesOutput]
        Required.
    links : ~analyticsapi.models.CollectionLinks
    """

    data: List["_models.CalculateDatesOutput"] = rest_field()
    """Required."""
    links: Optional["_models.CollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.CalculateDatesOutput"],
        links: Optional["_models.CollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class CountPeriodsOutput(_model_base.Model):
    """The result of the period calculation.

    Attributes
    ----------
    count : int
        The calculated number of dates in the period from startDate to endDate.
        Required.
    period_type : str or ~analyticsapi.models.PeriodTypeOutput
        The type of the calculated period. Required. Known values are: "Day",
        "WorkingDay", "Week", "Month", "Quarter", and "Year".
    processing_information : str
        Required.
    """

    count: int = rest_field()
    """The calculated number of dates in the period from startDate to endDate. Required."""
    period_type: Union[str, "_models.PeriodTypeOutput"] = rest_field(name="periodType")
    """The type of the calculated period. Required. Known values are: \"Day\", \"WorkingDay\",
     \"Week\", \"Month\", \"Quarter\", and \"Year\"."""
    processing_information: str = rest_field(name="processingInformation")
    """Required."""

    @overload
    def __init__(
        self,
        *,
        count: int,
        period_type: Union[str, "_models.PeriodTypeOutput"],
        processing_information: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CountPeriodsResponse(_model_base.Model):
    """CountPeriodsResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.CountPeriodsOutput
        Required.
    """

    data: "_models.CountPeriodsOutput" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        data: "_models.CountPeriodsOutput",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["data"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class CrossCurrencyAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of a cross currency.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CROSS_CURRENCY
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.CROSS_CURRENCY]] = rest_field(
        visibility=["read"], default=ResourceType.CROSS_CURRENCY
    )
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencyCollectionLinks(_model_base.Model):
    """CrossCurrencyCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencyCollectionResponse(_model_base.Model):
    """CrossCurrencyCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.CrossCurrencyAsCollectionItem]
        Required.
    links : ~analyticsapi.models.CrossCurrencyCollectionLinks
    """

    data: List["_models.CrossCurrencyAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.CrossCurrencyCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.CrossCurrencyAsCollectionItem"],
        links: Optional["_models.CrossCurrencyCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class CrossCurrencyDefinition(_model_base.Model):
    """The definition of the cross currency.

    Attributes
    ----------
    cross_scaling_factor : float
        The factor used for quoting cross currency rates. Minumum is 0.000001,
        maximum is 1000000, default is 1.
    swap_point_scaling_factor : float
        The factor used when quoting Swap cross currency rates (e.g., for
        'JPYUSD' it is 100). Minumum is 0.000001, maximum is 1000000, default
        is 10000.
    swap_point_precision : int
        The number of decimal places used for swap points.  Minumum is 0,
        maximum is 9.
    cross_rate_precision : int
        The number of decimal places used for cross rates.  Minumum is 0,
        maximum is 9.
    spot_lag : int
        The number of business days to settlement. If not provided, a default
        spot lag for the given code will be used, typically 2 business days.
    """

    cross_scaling_factor: Optional[float] = rest_field(name="crossScalingFactor")
    """The factor used for quoting cross currency rates. Minumum is 0.000001, maximum is 1000000,
     default is 1."""
    swap_point_scaling_factor: Optional[float] = rest_field(name="swapPointScalingFactor")
    """The factor used when quoting Swap cross currency rates (e.g., for 'JPYUSD' it is 100). Minumum
     is 0.000001, maximum is 1000000, default is 10000."""
    swap_point_precision: Optional[int] = rest_field(name="swapPointPrecision")
    """The number of decimal places used for swap points.  Minumum is 0, maximum is 9."""
    cross_rate_precision: Optional[int] = rest_field(name="crossRatePrecision")
    """The number of decimal places used for cross rates.  Minumum is 0, maximum is 9."""
    spot_lag: Optional[int] = rest_field(name="spotLag")
    """The number of business days to settlement. If not provided, a default spot lag for the given
     code will be used, typically 2 business days."""

    @overload
    def __init__(
        self,
        *,
        cross_scaling_factor: Optional[float] = None,
        swap_point_scaling_factor: Optional[float] = None,
        swap_point_precision: Optional[int] = None,
        cross_rate_precision: Optional[int] = None,
        spot_lag: Optional[int] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencyInput(_model_base.Model):
    """An object to specify a cross currency pair.

    Attributes
    ----------
    code : str
        The currency pair of FX Cross, expressed in ISO 4217 alphabetical
        format (e.g., 'EURCHF'). Required.
    """

    code: str = rest_field()
    """The currency pair of FX Cross, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF').
     Required."""

    @overload
    def __init__(
        self,
        code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class CrossCurrencyResource(_model_base.Model):
    """An object describing the basic properties of a resource on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CROSS_CURRENCY
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.CrossCurrencyDefinition
        Required.
    """

    type: Optional[Literal[ResourceType.CROSS_CURRENCY]] = rest_field(
        visibility=["read"], default=ResourceType.CROSS_CURRENCY
    )
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.CrossCurrencyDefinition" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.CrossCurrencyDefinition",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencyResponse(_model_base.Model):
    """CrossCurrencyResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.CrossCurrencyResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.CrossCurrencyResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.CrossCurrencyResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveConstituent(_model_base.Model):
    """The constituents that are used to construct the curve.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    CrossCurrencySwapConstituent, DepositConstituentFx, FxForwardConstituent, FxSpotConstituent

    Attributes
    ----------
    type : str or ~analyticsapi.models.FxForwardCurveConstituentType
        The type of instrument used as a constituent. Required. Known values
        are: "FxSpot", "FxForward", "CrossCurrencySwap", and "Deposit".
    definition : ~analyticsapi.models.FxConstituentDefinition
        The definition of the constituent.  Optional: provide either a
        definition or a quote.
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    quote : ~analyticsapi.models.QuoteInput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    type: str = rest_discriminator(name="type")
    """The type of instrument used as a constituent. Required. Known values are: \"FxSpot\",
     \"FxForward\", \"CrossCurrencySwap\", and \"Deposit\"."""
    definition: Optional["_models.FxConstituentDefinition"] = rest_field()
    """The definition of the constituent.  Optional: provide either a definition or a quote."""
    source: Optional[str] = rest_field()
    """The code of the contributor of the quote for the instrument used as a constituent (e.g.,
     'ICAP')."""
    quote: Optional["_models.QuoteInput"] = rest_field()
    """An object to define the quote of the instrument used as a constituent. Optional: provide either
     a definition or a quote."""

    @overload
    def __init__(
        self,
        *,
        type: str,
        definition: Optional["_models.FxConstituentDefinition"] = None,
        source: Optional[str] = None,
        quote: Optional["_models.QuoteInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencySwapConstituent(FxForwardCurveConstituent, discriminator="CrossCurrencySwap"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    quote : ~analyticsapi.models.QuoteInput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    type : str or ~analyticsapi.models.CROSS_CURRENCY_SWAP
        The type of instument used as a constituent.  CrossCurrencySwap is the
        only valid value. Required.
    definition : ~analyticsapi.models.CrossCurrencySwapConstituentDefinition
        An object to define the cross-currency swap instrument used as a
        constituent.
    """

    type: Literal[FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP] = rest_discriminator(name="type")  # type: ignore
    """The type of instument used as a constituent.  CrossCurrencySwap is the only valid value.
     Required."""
    definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = rest_field()
    """An object to define the cross-currency swap instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        quote: Optional["_models.QuoteInput"] = None,
        definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP, **kwargs)


class CrossCurrencySwapConstituentDefinition(_model_base.Model):
    """An object to define the cross-currency swap instrument used as a constituent.

    Attributes
    ----------
    tenor : str
        A tenor (relatvie date) expressed as a code, indicating the period
        covered by the constituent.
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    """

    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code, indicating the period covered by the constituent."""
    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The currency pair, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF'). Required."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        tenor: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveConstituentValues(_model_base.Model):
    """An object specifying values for FxForward curve constituents.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    CrossCurrencySwapConstituentValues, DepositConstituentValuesFx, FxForwardConstituentValues,
    FxSpotConstituentValues

    Attributes
    ----------
    type : str or ~analyticsapi.models.FxForwardCurveConstituentType
        The FX Forward curve constituent type. Required. Known values are:
        "FxSpot", "FxForward", "CrossCurrencySwap", and "Deposit".
    definition : ~analyticsapi.models.FxConstituentDefinition
        The definition of the constituent.  Optional: provide either a
        definition or a quote.
    quote : ~analyticsapi.models.QuoteOutput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    status_message : str
        The status of the constituent.
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    type: str = rest_discriminator(name="type")
    """The FX Forward curve constituent type. Required. Known values are: \"FxSpot\", \"FxForward\",
     \"CrossCurrencySwap\", and \"Deposit\"."""
    definition: Optional["_models.FxConstituentDefinition"] = rest_field()
    """The definition of the constituent.  Optional: provide either a definition or a quote."""
    quote: Optional["_models.QuoteOutput"] = rest_field()
    """An object to define the quote of the instrument used as a constituent. Optional: provide either
     a definition or a quote."""
    status_message: Optional[str] = rest_field(name="statusMessage")
    """The status of the constituent."""

    @overload
    def __init__(
        self,
        *,
        type: str,
        definition: Optional["_models.FxConstituentDefinition"] = None,
        quote: Optional["_models.QuoteOutput"] = None,
        status_message: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencySwapConstituentValues(FxForwardCurveConstituentValues, discriminator="CrossCurrencySwap"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    quote : ~analyticsapi.models.QuoteOutput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.CROSS_CURRENCY_SWAP
        The type of instument used as a constituent.  CrossCurrencySwap is the
        only valid value. Required.
    definition : ~analyticsapi.models.CrossCurrencySwapConstituentDefinition
        An object to define the cross-currency swap instrument used as a
        constituent.
    """

    type: Literal[FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP] = rest_discriminator(name="type")  # type: ignore
    """The type of instument used as a constituent.  CrossCurrencySwap is the only valid value.
     Required."""
    definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = rest_field()
    """An object to define the cross-currency swap instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        quote: Optional["_models.QuoteOutput"] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP, **kwargs)


class FxInvalidConstituent(_model_base.Model):
    """An object describing an invalid Fx constituent.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    CrossCurrencySwapInvalidConstituent, DepositInvalidConstituentFx, FxForwardInvalidConstituent,
    FxSpotInvalidConstituent

    Attributes
    ----------
    type : str or ~analyticsapi.models.FxForwardCurveConstituentType
        FX Forward curve constituent type. Required. Known values are:
        "FxSpot", "FxForward", "CrossCurrencySwap", and "Deposit".
    definition : ~analyticsapi.models.FxConstituentDefinition
        The definition of the constituent.
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    status_message : str
        The status of the constituent.
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    type: str = rest_discriminator(name="type")
    """FX Forward curve constituent type. Required. Known values are: \"FxSpot\", \"FxForward\",
     \"CrossCurrencySwap\", and \"Deposit\"."""
    definition: Optional["_models.FxConstituentDefinition"] = rest_field()
    """The definition of the constituent."""
    source: Optional[str] = rest_field()
    """The code of the contributor of the quote for the instrument used as a constituent (e.g.,
     'ICAP')."""
    status_message: Optional[str] = rest_field(name="statusMessage")
    """The status of the constituent."""

    @overload
    def __init__(
        self,
        *,
        type: str,
        definition: Optional["_models.FxConstituentDefinition"] = None,
        source: Optional[str] = None,
        status_message: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CrossCurrencySwapInvalidConstituent(FxInvalidConstituent, discriminator="CrossCurrencySwap"):
    """CrossCurrencySwapInvalidConstituent.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.CROSS_CURRENCY_SWAP
        Required.
    definition : ~analyticsapi.models.CrossCurrencySwapConstituentDefinition
    """

    type: Literal[FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP] = rest_discriminator(name="type")  # type: ignore
    """Required."""
    definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.CrossCurrencySwapConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.CROSS_CURRENCY_SWAP, **kwargs)


class CurrencyAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of a currency.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CURRENCY
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.CURRENCY]] = rest_field(visibility=["read"], default=ResourceType.CURRENCY)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CurrencyCollectionLinks(_model_base.Model):
    """CurrencyCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CurrencyCollectionResponse(_model_base.Model):
    """CurrencyCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.CurrencyAsCollectionItem]
        Required.
    links : ~analyticsapi.models.CurrencyCollectionLinks
    """

    data: List["_models.CurrencyAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.CurrencyCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.CurrencyAsCollectionItem"],
        links: Optional["_models.CurrencyCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class CurrencyDefinition(_model_base.Model):
    """The definition of the currency pair.

    Attributes
    ----------
    spot_lag : int
        The number of business days to settlement. The minimum is 0. If not
        provided, a default spot lag for the given code will be used, typically
        2 business days. Required.
    year_basis : str or ~analyticsapi.models.YearBasis
        The number of days in a year. Required. Known values are: "360" and
        "365".
    calendar : ~analyticsapi.models.CalendarRelatedResource
        Related calendar. Required.
    """

    spot_lag: int = rest_field(name="spotLag")
    """The number of business days to settlement. The minimum is 0. If not provided, a default spot
     lag for the given code will be used, typically 2 business days. Required."""
    year_basis: Union[str, "_models.YearBasis"] = rest_field(name="yearBasis")
    """The number of days in a year. Required. Known values are: \"360\" and \"365\"."""
    calendar: "_models.CalendarRelatedResource" = rest_field()
    """Related calendar. Required."""

    @overload
    def __init__(
        self,
        *,
        spot_lag: int,
        year_basis: Union[str, "_models.YearBasis"],
        calendar: "_models.CalendarRelatedResource",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CurrencyInput(_model_base.Model):
    """An object to specify a currency.

    Attributes
    ----------
    code : str
        The currency expressed in ISO 4217 alphabetical format (e.g., 'EUR').
        Required.
    """

    code: str = rest_field()
    """The currency expressed in ISO 4217 alphabetical format (e.g., 'EUR'). Required."""

    @overload
    def __init__(
        self,
        code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class CurrencyResource(_model_base.Model):
    """An object describing the basic properties of a resource on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.CURRENCY
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.CurrencyDefinition
        Required.
    """

    type: Optional[Literal[ResourceType.CURRENCY]] = rest_field(visibility=["read"], default=ResourceType.CURRENCY)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.CurrencyDefinition" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.CurrencyDefinition",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CurrencyResponse(_model_base.Model):
    """CurrencyResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.CurrencyResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.CurrencyResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.CurrencyResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class CurvePointRelatedInstruments(_model_base.Model):
    """An object that contains the instrument used to calculate the curve point.

    Attributes
    ----------
    instrument_code : str
        The identifier of the instrument used to calculate the curve point.
        Required.
    """

    instrument_code: str = rest_field(name="instrumentCode")
    """The identifier of the instrument used to calculate the curve point. Required."""

    @overload
    def __init__(
        self,
        instrument_code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["instrument_code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class DepositConstituentDefinition(_model_base.Model):
    """An object to define the deposit instrument used as a constituent.

    Attributes
    ----------
    tenor : str
        A tenor (relatvie date) expressed as a code, indicating the period
        covered by the constituent.
    currency : ~analyticsapi.models.CurrencyInput
        The currency of the instrument expressed in ISO 4217 alphabetical
        format (e.g., 'EUR'). Required.
    template : str
    """

    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code, indicating the period covered by the constituent."""
    currency: "_models.CurrencyInput" = rest_field()
    """The currency of the instrument expressed in ISO 4217 alphabetical format (e.g., 'EUR').
     Required."""
    template: Optional[str] = rest_field()

    @overload
    def __init__(
        self,
        *,
        currency: "_models.CurrencyInput",
        tenor: Optional[str] = None,
        template: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class DepositConstituentFx(FxForwardCurveConstituent, discriminator="Deposit"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    quote : ~analyticsapi.models.QuoteInput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    type : str or ~analyticsapi.models.DEPOSIT
        The type of constituent.  Deposit is the only valid value. Required.
    definition : ~analyticsapi.models.DepositConstituentDefinition
        An object to define the deposit instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.DEPOSIT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  Deposit is the only valid value. Required."""
    definition: Optional["_models.DepositConstituentDefinition"] = rest_field()
    """An object to define the deposit instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        quote: Optional["_models.QuoteInput"] = None,
        definition: Optional["_models.DepositConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.DEPOSIT, **kwargs)


class DepositConstituentValuesFx(FxForwardCurveConstituentValues, discriminator="Deposit"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    quote : ~analyticsapi.models.QuoteOutput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.DEPOSIT
        The type of constituent.  Deposit is the only valid value. Required.
    definition : ~analyticsapi.models.DepositConstituentDefinition
        An object to define the deposit instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.DEPOSIT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  Deposit is the only valid value. Required."""
    definition: Optional["_models.DepositConstituentDefinition"] = rest_field()
    """An object to define the deposit instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        quote: Optional["_models.QuoteOutput"] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.DepositConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.DEPOSIT, **kwargs)


class DepositInvalidConstituentFx(FxInvalidConstituent, discriminator="Deposit"):
    """DepositInvalidConstituentFx.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.DEPOSIT
        The type of constituent.  Deposit is the only valid value. Required.
    definition : ~analyticsapi.models.DepositConstituentDefinition
        An object to define the deposit instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.DEPOSIT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  Deposit is the only valid value. Required."""
    definition: Optional["_models.DepositConstituentDefinition"] = rest_field()
    """An object to define the deposit instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.DepositConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.DEPOSIT, **kwargs)


class Description(_model_base.Model):
    """A description and up to 5 tags for a resource.

    Attributes
    ----------
    summary : str
        A summary of information about the resource. Limited to 500 characters.
    tags : list[str]
        User-defined tags to identify the resource. Limited to 5 items and 50
        characters each.
    """

    summary: Optional[str] = rest_field()
    """A summary of information about the resource. Limited to 500 characters."""
    tags: Optional[List[str]] = rest_field()
    """User-defined tags to identify the resource. Limited to 5 items and 50 characters each."""

    @overload
    def __init__(
        self,
        *,
        summary: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.tags is None:
            self.tags = list()


class Duration(_model_base.Model):
    """An object to determine the duration of the holiday.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    FullDayDuration, HalfDayDuration

    Attributes
    ----------
    duration_type : str or ~analyticsapi.models.DurationType
        The type of the holiday duration. Possible values are: FullDayDuration
        or HalfDayDuration. Required. Known values are: "FullDayDuration" and
        "HalfDayDuration".
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    duration_type: str = rest_discriminator(name="durationType")
    """The type of the holiday duration. Possible values are: FullDayDuration or HalfDayDuration.
     Required. Known values are: \"FullDayDuration\" and \"HalfDayDuration\"."""

    @overload
    def __init__(
        self,
        duration_type: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["duration_type"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class FieldValue(_model_base.Model):
    """An object that contains the bid and ask quotes and related attributes for the instrument.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    value : float
        The quote value of the instrument. Required.
    is_overridden : bool
        An indicator whether the value is overridden. It returns only 'true' if
        value is overridden in the request.
    market_value : float
        The quote retrieved from the market. It is returned in the response
        only if the value is overridden in the request.
    """

    value: float = rest_field()
    """The quote value of the instrument. Required."""
    is_overridden: Optional[bool] = rest_field(name="isOverridden", visibility=["read"])
    """An indicator whether the value is overridden. It returns only 'true' if value is overridden in
     the request."""
    market_value: Optional[float] = rest_field(name="marketValue", visibility=["read"])
    """The quote retrieved from the market. It is returned in the response only if the value is
     overridden in the request."""

    @overload
    def __init__(
        self,
        value: float,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FullDayDuration(Duration, discriminator="FullDayDuration"):
    """An object to determine the duration of the holiday in full days.

    Attributes
    ----------
    duration_type : str or ~analyticsapi.models.FULL_DAY_DURATION
        The type of the holiday duration. Only FullDayDuration value applies.
        Required. Full days where the no trading takes place.
    full_day : int
        The duration of the holiday as a number of full calendar days. The
        minimum value is 1. Required.
    """

    duration_type: Literal[DurationType.FULL_DAY_DURATION] = rest_discriminator(name="durationType")  # type: ignore
    """The type of the holiday duration. Only FullDayDuration value applies. Required. Full days where
     the no trading takes place."""
    full_day: int = rest_field(name="fullDay")
    """The duration of the holiday as a number of full calendar days. The minimum value is 1.
     Required."""

    @overload
    def __init__(
        self,
        full_day: int,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, duration_type=DurationType.FULL_DAY_DURATION, **kwargs)


class FxAnalyticsDescription(_model_base.Model):
    """The analytics fields that describe the instrument.

    Attributes
    ----------
    valuation_date : ~datetime.date
        The date at which the instrument is valued. The date is expressed in
        ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        '2021-01-01T00:00:00Z').
    start_date : ~analyticsapi.models.AdjustedDate
        The start date of the instrument.
    end_date : ~analyticsapi.models.AdjustedDate
        The maturity date of the instrument.
    """

    valuation_date: Optional[datetime.date] = rest_field(name="valuationDate")
    """The date at which the instrument is valued. The date is expressed in ISO 8601 format:
     YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g., '2021-01-01T00:00:00Z')."""
    start_date: Optional["_models.AdjustedDate"] = rest_field(name="startDate")
    """The start date of the instrument."""
    end_date: Optional["_models.AdjustedDate"] = rest_field(name="endDate")
    """The maturity date of the instrument."""

    @overload
    def __init__(
        self,
        *,
        valuation_date: Optional[datetime.date] = None,
        start_date: Optional["_models.AdjustedDate"] = None,
        end_date: Optional["_models.AdjustedDate"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxConstituentDefinition(_model_base.Model):
    """An object to define the FX instrument used as a constituent.

    Attributes
    ----------
    tenor : str
        A tenor (relatvie date) expressed as a code, indicating the period
        covered by the constituent.
    """

    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code, indicating the period covered by the constituent."""

    @overload
    def __init__(
        self,
        tenor: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["tenor"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class FxForwardAnalyticsDescription(FxAnalyticsDescription):
    """The analytic fields that describe the instrument.

    Attributes
    ----------
    valuation_date : ~datetime.date
        The date at which the instrument is valued. The date is expressed in
        ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        '2021-01-01T00:00:00Z').
    start_date : ~analyticsapi.models.AdjustedDate
        The start date of the instrument.
    end_date : ~analyticsapi.models.AdjustedDate
        The maturity date of the instrument.
    """

    @overload
    def __init__(
        self,
        *,
        valuation_date: Optional[datetime.date] = None,
        start_date: Optional["_models.AdjustedDate"] = None,
        end_date: Optional["_models.AdjustedDate"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardAnalyticsPricing(_model_base.Model):
    """Object defining the output of a FX Forward pricing analysis.

    Attributes
    ----------
    description : ~analyticsapi.models.FxForwardAnalyticsDescription
        The analytic fields that describe the instrument.
    pricing_analysis : ~analyticsapi.models.FxForwardPricingAnalysis
        The analytic fields that are linked to a pre-trade analysis of the
        instrument.
    greeks : ~analyticsapi.models.FxForwardRisk
        The analytic fields that are linked to a risk analysis of the
        instrument.
    """

    description: Optional["_models.FxForwardAnalyticsDescription"] = rest_field()
    """The analytic fields that describe the instrument."""
    pricing_analysis: Optional["_models.FxForwardPricingAnalysis"] = rest_field(name="pricingAnalysis")
    """The analytic fields that are linked to a pre-trade analysis of the instrument."""
    greeks: Optional["_models.FxForwardRisk"] = rest_field()
    """The analytic fields that are linked to a risk analysis of the instrument."""

    @overload
    def __init__(
        self,
        *,
        description: Optional["_models.FxForwardAnalyticsDescription"] = None,
        pricing_analysis: Optional["_models.FxForwardPricingAnalysis"] = None,
        greeks: Optional["_models.FxForwardRisk"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardAnalyticsValuation(_model_base.Model):
    """Object defining the output of a FX Forward valuation analysis.

    Attributes
    ----------
    description : ~analyticsapi.models.FxForwardAnalyticsDescription
        The analytic fields that describe the instrument.
    valuation : ~analyticsapi.models.FxForwardValuation
    greeks : ~analyticsapi.models.FxForwardRisk
        The analytic fields that are linked to a risk analysis of the
        instrument.
    """

    description: Optional["_models.FxForwardAnalyticsDescription"] = rest_field()
    """The analytic fields that describe the instrument."""
    valuation: Optional["_models.FxForwardValuation"] = rest_field()
    greeks: Optional["_models.FxForwardRisk"] = rest_field()
    """The analytic fields that are linked to a risk analysis of the instrument."""

    @overload
    def __init__(
        self,
        *,
        description: Optional["_models.FxForwardAnalyticsDescription"] = None,
        valuation: Optional["_models.FxForwardValuation"] = None,
        greeks: Optional["_models.FxForwardRisk"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of a FX forward.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.FX_FORWARD]] = rest_field(visibility=["read"], default=ResourceType.FX_FORWARD)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCollectionLinks(_model_base.Model):
    """FxForwardCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCollectionResponse(_model_base.Model):
    """FxForwardCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.FxForwardAsCollectionItem]
        Required.
    links : ~analyticsapi.models.FxForwardCollectionLinks
    """

    data: List["_models.FxForwardAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.FxForwardCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.FxForwardAsCollectionItem"],
        links: Optional["_models.FxForwardCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class FxForwardConstituent(FxForwardCurveConstituent, discriminator="FxForward"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    quote : ~analyticsapi.models.QuoteInput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    type : str or ~analyticsapi.models.FX_FORWARD
        The type of constituent.  FxForward is the only valid value. Required.
    definition : ~analyticsapi.models.FxForwardConstituentDefinition
        An object to define the FX forward instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_FORWARD] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxForward is the only valid value. Required."""
    definition: Optional["_models.FxForwardConstituentDefinition"] = rest_field()
    """An object to define the FX forward instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        quote: Optional["_models.QuoteInput"] = None,
        definition: Optional["_models.FxForwardConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_FORWARD, **kwargs)


class FxForwardConstituentDefinition(_model_base.Model):
    """An object to define the FX forward instrument used as a constituent.

    Attributes
    ----------
    tenor : str
        A tenor (relatvie date) expressed as a code, indicating the period
        covered by the constituent.
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    """

    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code, indicating the period covered by the constituent."""
    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The currency pair, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF'). Required."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        tenor: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardConstituentValues(FxForwardCurveConstituentValues, discriminator="FxForward"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    quote : ~analyticsapi.models.QuoteOutput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.FX_FORWARD
        The type of constituent.  FxForward is the only valid value. Required.
    definition : ~analyticsapi.models.FxForwardConstituentDefinition
        An object to define the FX forward instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_FORWARD] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxForward is the only valid value. Required."""
    definition: Optional["_models.FxForwardConstituentDefinition"] = rest_field()
    """An object to define the FX forward instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        quote: Optional["_models.QuoteOutput"] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.FxForwardConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_FORWARD, **kwargs)


class FxForwardCurveAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of a FX forward curve.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveDefinition(_model_base.Model):
    """An object to define the Fx Forward Curve resource.

    Attributes
    ----------
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    reference_currency : ~analyticsapi.models.CurrencyInput
        The currency of the curve expressed in ISO 4217 alphabetical format
        (e.g., 'EUR').
    constituents : list[~analyticsapi.models.FxForwardCurveConstituent]
        An array of objects to define constituents that are used to construct
        the curve.

        * If there is a reference currency there must be two constituents.
        * If there is no reference currency there must be one constituent.
    """

    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The currency pair, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF'). Required."""
    reference_currency: Optional["_models.CurrencyInput"] = rest_field(name="referenceCurrency")
    """The currency of the curve expressed in ISO 4217 alphabetical format (e.g., 'EUR')."""
    constituents: Optional[List["_models.FxForwardCurveConstituent"]] = rest_field()
    """An array of objects to define constituents that are used to construct the curve.
     
     
     * If there is a reference currency there must be two constituents.
     * If there is no reference currency there must be one constituent."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        reference_currency: Optional["_models.CurrencyInput"] = None,
        constituents: Optional[List["_models.FxForwardCurveConstituent"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.constituents is None:
            self.constituents = list()


class FxForwardCurveAsMarketDataInput(FxForwardCurveDefinition):
    """Object describing the FX forward curve used for the calculation.

    Attributes
    ----------
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    reference_currency : ~analyticsapi.models.CurrencyInput
        The currency of the curve expressed in ISO 4217 alphabetical format
        (e.g., 'EUR').
    constituents : list[~analyticsapi.models.FxForwardCurveConstituent]
        An array of objects to define constituents that are used to construct
        the curve.

        * If there is a reference currency there must be two constituents.
        * If there is no reference currency there must be one constituent.
    template : ~analyticsapi.models.FxForwardCurveRelatedResource
        Object identifying a resource by either uuid or location (space and
        name).
    """

    template: Optional["_models.FxForwardCurveRelatedResource"] = rest_field()
    """Object identifying a resource by either uuid or location (space and name)."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        reference_currency: Optional["_models.CurrencyInput"] = None,
        constituents: Optional[List["_models.FxForwardCurveConstituent"]] = None,
        template: Optional["_models.FxForwardCurveRelatedResource"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["template"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)
        if self.constituents is None:
            self.constituents = list()


class FxForwardCurveAsMarketDataOutput(_model_base.Model):
    """FxForwardCurveAsMarketDataOutput.

    Attributes
    ----------
    data : list[~analyticsapi.models.FxForwardCurvePoint]
    definition : ~analyticsapi.models.FxForwardCurveDefinition
    """

    data: Optional[List["_models.FxForwardCurvePoint"]] = rest_field()
    definition: Optional["_models.FxForwardCurveDefinition"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: Optional[List["_models.FxForwardCurvePoint"]] = None,
        definition: Optional["_models.FxForwardCurveDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class FxForwardCurveAsTransient(_model_base.Model):
    """TransientResources are bare definitions of the resources.
    They don't have an id, location and description since they are used on the fly and are not
    stored on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
    definition : ~analyticsapi.models.FxForwardCurveDefinition
        Required.
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    definition: "_models.FxForwardCurveDefinition" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        definition: "_models.FxForwardCurveDefinition",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCalculateOnTheFlyResponse(_model_base.Model):
    """FxForwardCurveCalculateOnTheFlyResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardCurveOnTheFlyCalculationContext
    data : ~analyticsapi.models.FxForwardCurveData
    """

    context: Optional["_models.FxForwardCurveOnTheFlyCalculationContext"] = rest_field()
    data: Optional["_models.FxForwardCurveData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardCurveOnTheFlyCalculationContext"] = None,
        data: Optional["_models.FxForwardCurveData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCalculateResponse(_model_base.Model):
    """FxForwardCurveCalculateResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardCurveCalculationContext
    data : ~analyticsapi.models.FxForwardCurveData
    """

    context: Optional["_models.FxForwardCurveCalculationContext"] = rest_field()
    data: Optional["_models.FxForwardCurveData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardCurveCalculationContext"] = None,
        data: Optional["_models.FxForwardCurveData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCalculationContext(_model_base.Model):
    """FxForwardCurveCalculationContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxForwardCurveDefinition
        Required.
    parameters : ~analyticsapi.models.FxForwardCurvePricingParameters
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxForwardCurveDefinition" = rest_field()
    """Required."""
    parameters: Optional["_models.FxForwardCurvePricingParameters"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxForwardCurveDefinition",
        description: Optional["_models.Description"] = None,
        parameters: Optional["_models.FxForwardCurvePricingParameters"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCalculationPreferences(_model_base.Model):
    """An object to define calculation preferences for the curve.

    Attributes
    ----------
    extrapolation_mode : str or ~analyticsapi.models.ExtrapolationMode
        The extrapolation method used in the curve bootstrapping. The default
        is None. Known values are: "None", "Constant", and "Linear".
    interpolation_mode : str or ~analyticsapi.models.FxForwardCurveInterpolationMode
        The interpolation method used in the curve bootstrapping. The default
        is Linear. Known values are: "CubicSpline", "Constant", "Linear", and
        "CubicDiscount".
    use_delayed_data_if_denied : bool
        Set to true to use the delayed data defined in the request. The default
        is false.
    ignore_invalid_instruments : bool
        Set to true to ignore invalid instruments in the curve construction.
        The default is false.
    adjust_all_deposit_points_to_cross_calendars : bool
        Set to true to adjust deposit points to the cross-calendar dates. The
        default is true.
    adjust_all_swap_points_to_cross_calendars : bool
        Set to true to adjust swap points to the cross-calendar dates. The
        default is true.
    ignore_pivot_currency_holidays : bool
        Set to true to include holidays of the pivot currency in the pricing
        when dates are calculated. The default is false.
    """

    extrapolation_mode: Optional[Union[str, "_models.ExtrapolationMode"]] = rest_field(name="extrapolationMode")
    """The extrapolation method used in the curve bootstrapping. The default is None. Known values
     are: \"None\", \"Constant\", and \"Linear\"."""
    interpolation_mode: Optional[Union[str, "_models.FxForwardCurveInterpolationMode"]] = rest_field(
        name="interpolationMode"
    )
    """The interpolation method used in the curve bootstrapping. The default is Linear. Known values
     are: \"CubicSpline\", \"Constant\", \"Linear\", and \"CubicDiscount\"."""
    use_delayed_data_if_denied: Optional[bool] = rest_field(name="useDelayedDataIfDenied")
    """Set to true to use the delayed data defined in the request. The default is false."""
    ignore_invalid_instruments: Optional[bool] = rest_field(name="ignoreInvalidInstruments")
    """Set to true to ignore invalid instruments in the curve construction. The default is false."""
    adjust_all_deposit_points_to_cross_calendars: Optional[bool] = rest_field(
        name="adjustAllDepositPointsToCrossCalendars"
    )
    """Set to true to adjust deposit points to the cross-calendar dates. The default is true."""
    adjust_all_swap_points_to_cross_calendars: Optional[bool] = rest_field(name="adjustAllSwapPointsToCrossCalendars")
    """Set to true to adjust swap points to the cross-calendar dates. The default is true."""
    ignore_pivot_currency_holidays: Optional[bool] = rest_field(name="ignorePivotCurrencyHolidays")
    """Set to true to include holidays of the pivot currency in the pricing when dates are calculated.
     The default is false."""

    @overload
    def __init__(
        self,
        *,
        extrapolation_mode: Optional[Union[str, "_models.ExtrapolationMode"]] = None,
        interpolation_mode: Optional[Union[str, "_models.FxForwardCurveInterpolationMode"]] = None,
        use_delayed_data_if_denied: Optional[bool] = None,
        ignore_invalid_instruments: Optional[bool] = None,
        adjust_all_deposit_points_to_cross_calendars: Optional[bool] = None,
        adjust_all_swap_points_to_cross_calendars: Optional[bool] = None,
        ignore_pivot_currency_holidays: Optional[bool] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCollectionLinks(_model_base.Model):
    """FxForwardCurveCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveCollectionResponse(_model_base.Model):
    """FxForwardCurveCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.FxForwardCurveAsCollectionItem]
        Required.
    links : ~analyticsapi.models.FxForwardCurveCollectionLinks
    """

    data: List["_models.FxForwardCurveAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.FxForwardCurveCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.FxForwardCurveAsCollectionItem"],
        links: Optional["_models.FxForwardCurveCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class FxForwardCurveData(_model_base.Model):
    """An object that describes the constructed curve.

    Attributes
    ----------
    curve : ~analyticsapi.models.FxForwardCurveOutput
        An object that describes the constructed curve surface. Required.
    """

    curve: "_models.FxForwardCurveOutput" = rest_field()
    """An object that describes the constructed curve surface. Required."""

    @overload
    def __init__(
        self,
        curve: "_models.FxForwardCurveOutput",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["curve"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class FxForwardCurveOnTheFlyCalculationContext(_model_base.Model):
    """FxForwardCurveOnTheFlyCalculationContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
    definition : ~analyticsapi.models.FxForwardCurveDefinition
        Required.
    parameters : ~analyticsapi.models.FxForwardCurvePricingParameters
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    definition: "_models.FxForwardCurveDefinition" = rest_field()
    """Required."""
    parameters: Optional["_models.FxForwardCurvePricingParameters"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        definition: "_models.FxForwardCurveDefinition",
        parameters: Optional["_models.FxForwardCurvePricingParameters"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveOutput(_model_base.Model):
    """An object that describes the constructed curve surface.

    Attributes
    ----------
    constituents : list[~analyticsapi.models.FxForwardCurveConstituentValues]
        An array of objects to define constituents that are used to construct
        the curve.
    curve_points : list[~analyticsapi.models.FxForwardCurvePoint]
        An array of objects that contains curve points and related attributes
        of the curve.
    underlying_curves : ~analyticsapi.models.UnderlyingCurves
        An object that contains the underlying curves surfaces used to
        construct the curve.
    invalid_constituents : list[~analyticsapi.models.FxInvalidConstituent]
    """

    constituents: Optional[List["_models.FxForwardCurveConstituentValues"]] = rest_field()
    """An array of objects to define constituents that are used to construct the curve."""
    curve_points: Optional[List["_models.FxForwardCurvePoint"]] = rest_field(name="curvePoints")
    """An array of objects that contains curve points and related attributes of the curve."""
    underlying_curves: Optional["_models.UnderlyingCurves"] = rest_field(name="underlyingCurves")
    """An object that contains the underlying curves surfaces used to construct the curve."""
    invalid_constituents: Optional[List["_models.FxInvalidConstituent"]] = rest_field(name="invalidConstituents")

    @overload
    def __init__(
        self,
        *,
        constituents: Optional[List["_models.FxForwardCurveConstituentValues"]] = None,
        curve_points: Optional[List["_models.FxForwardCurvePoint"]] = None,
        underlying_curves: Optional["_models.UnderlyingCurves"] = None,
        invalid_constituents: Optional[List["_models.FxInvalidConstituent"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.constituents is None:
            self.constituents = list()
        if self.curve_points is None:
            self.curve_points = list()
        if self.invalid_constituents is None:
            self.invalid_constituents = list()


class FxForwardCurvePoint(_model_base.Model):
    """An object that contains the values applied to the FX Forward curve point.

    Attributes
    ----------
    tenor : str
        A code indicating the length of the period between the start date and
        the end date of the curve point. Predefined values are: ON (Overnight -
        A one business day period that starts today), TN (Tomorrow-Next - A one
        business day period that starts next business day, SPOT (Spot Date), SN
        (Spot-Next - A one business day period that starts at the spot date of
        a currency pair) or SW (Spot-Week - A one business week period that
        starts at the spot date of a currency pair). Tenors can also be
        specified as a whole number of time units. Possible units are: D
        (Days), W (Weeks), M (Months) or Y (Years). For example, one month is
        written '1M', 3 years is written: '3Y'. Time units can be mixed. For
        example, 5M3D means '5 months and 3 days'. Note: units must be written
        in descending order of size (Y > M > W > D). Required.
    start_date : ~datetime.date
        The start date of the curve point tenor. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., '2023-01-01'). Required.
    end_date : ~datetime.date
        The end date of the curve point tenor. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., '2024-01-01'). Required.
    instruments : list[~analyticsapi.models.CurvePointRelatedInstruments]
        An array of objects that contains instruments used to calculate the
        curve point.
    swap_point : ~analyticsapi.models.BidAskMidSimpleValues
        The swap point calculated for a given curve point. Required.
    outright : ~analyticsapi.models.BidAskMidSimpleValues
        The outright calculated for a given curve point. Required.
    """

    tenor: str = rest_field()
    """A code indicating the length of the period between the start date and the end date of the curve
     point.
     Predefined values are: ON (Overnight - A one business day period that starts today), TN
     (Tomorrow-Next - A one business day period that starts next business day, SPOT (Spot Date), SN
     (Spot-Next - A one business day period that starts at the spot date of a currency pair) or SW
     (Spot-Week - A one business week period that starts at the spot date of a currency pair).
     Tenors can also be specified as a whole number of time units. Possible units are: D (Days), W
     (Weeks), M (Months) or Y (Years). For example, one month is written '1M', 3 years is written:
     '3Y'.
     Time units can be mixed. For example, 5M3D means '5 months and 3 days'. Note: units must be
     written in descending order of size (Y > M > W > D). Required."""
    start_date: datetime.date = rest_field(name="startDate")
    """The start date of the curve point tenor. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., '2023-01-01'). Required."""
    end_date: datetime.date = rest_field(name="endDate")
    """The end date of the curve point tenor. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., '2024-01-01'). Required."""
    instruments: Optional[List["_models.CurvePointRelatedInstruments"]] = rest_field()
    """An array of objects that contains instruments used to calculate the curve point."""
    swap_point: "_models.BidAskMidSimpleValues" = rest_field(name="swapPoint")
    """The swap point calculated for a given curve point. Required."""
    outright: "_models.BidAskMidSimpleValues" = rest_field()
    """The outright calculated for a given curve point. Required."""

    @overload
    def __init__(
        self,
        *,
        tenor: str,
        start_date: datetime.date,
        end_date: datetime.date,
        swap_point: "_models.BidAskMidSimpleValues",
        outright: "_models.BidAskMidSimpleValues",
        instruments: Optional[List["_models.CurvePointRelatedInstruments"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instruments is None:
            self.instruments = list()


class FxForwardCurvePricingParameters(_model_base.Model):
    """An object that contains parameters used to define how the Fx Forward curve is constructed from
    the constituents.

    Attributes
    ----------
    valuation_date : ~datetime.date
        The date on which the curve is constructed. The value is expressed in
        ISO 8601 format: YYYY-MM-DD (e.g., '2023-01-01'). The valuation date
        should not be in the future. Default is Today.
    fx_forward_curve_calculation_preferences : ~analyticsapi.models.FxForwardCurveCalculationPreferences
        An object to define calculation preferences for the curve.
    """

    valuation_date: Optional[datetime.date] = rest_field(name="valuationDate")
    """The date on which the curve is constructed. The value is expressed in ISO 8601 format:
     YYYY-MM-DD (e.g., '2023-01-01').
     The valuation date should not be in the future. Default is Today."""
    fx_forward_curve_calculation_preferences: Optional["_models.FxForwardCurveCalculationPreferences"] = rest_field(
        name="fxForwardCurveCalculationPreferences"
    )
    """An object to define calculation preferences for the curve."""

    @overload
    def __init__(
        self,
        *,
        valuation_date: Optional[datetime.date] = None,
        fx_forward_curve_calculation_preferences: Optional["_models.FxForwardCurveCalculationPreferences"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveRelatedResource(_model_base.Model):
    """Object identifying a resource by either uuid or location (space and name).

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
        The type of the resource.
    id : str
        The unique id of the resource.
    location : ~analyticsapi.models.Location
        An object to define the location of the resource (space and name).
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    """The type of the resource."""
    id: Optional[str] = rest_field()
    """The unique id of the resource."""
    location: Optional["_models.Location"] = rest_field()
    """An object to define the location of the resource (space and name)."""

    @overload
    def __init__(
        self,
        *,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        location: Optional["_models.Location"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveResource(_model_base.Model):
    """An object describing the basic properties of a resource on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD_CURVE
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxForwardCurveDefinition
        Required.
    """

    type: Optional[Literal[ResourceType.FX_FORWARD_CURVE]] = rest_field(
        visibility=["read"], default=ResourceType.FX_FORWARD_CURVE
    )
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxForwardCurveDefinition" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxForwardCurveDefinition",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardCurveResponse(_model_base.Model):
    """FxForwardCurveResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.FxForwardCurveResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.FxForwardCurveResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.FxForwardCurveResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxPayment(_model_base.Model):
    """Definition of a Fx Spot.

    Attributes
    ----------
    fx_rate : ~analyticsapi.models.FxRate
        An object defining the FX rate. Required.
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the deal (base)
        currency.
    """

    fx_rate: "_models.FxRate" = rest_field(name="fxRate")
    """An object defining the FX rate. Required."""
    deal_amount: Optional[float] = rest_field(name="dealAmount")
    """The amount of the deal (base) currency bought or sold."""
    contra_amount: Optional[float] = rest_field(name="contraAmount")
    """The amount of contra currency exchanged to buy or sell the deal (base) currency."""

    @overload
    def __init__(
        self,
        *,
        fx_rate: "_models.FxRate",
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardInstrument(FxPayment):
    """The definition of a FX forward instrument.

    Attributes
    ----------
    fx_rate : ~analyticsapi.models.FxRate
        An object defining the FX rate. Required.
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the deal (base)
        currency.
    end_date : ~analyticsapi.models.Date
        The maturity date of the instrument. Possible values are: An adjustable
        date - requires a date expressed in ISO 8601 format: YYYY-MM-
        DDT[hh]:[mm]:[ss]Z (e.g., '2021-01-01T00:00:00Z'). Or a relative
        adjustable date - requires a tenor expressed as a code indicating the
        period between the reference date (default reference date is the start
        date) and the end date of the instrument (e.g. '6M', '1Y'). Required.
    start_date : ~analyticsapi.models.Date
        The start date of the instrument. Possible values are: An adjustable
        date - requires a date expressed in ISO 8601 format: YYYY-MM-
        DDT[hh]:[mm]:[ss]Z (e.g., '2021-01-01T00:00:00Z'). Or a relative
        adjustable date - requires a tenor expressed as a code indicating the
        period between the reference date (default reference date is the start
        date) and the end date of the instrument (e.g. '6M', '1Y'). Default is
        the spot date.
    settlement_type : str or ~analyticsapi.models.SettlementType
        How the instrument is settled.  Possible values are: Physical or Cash.
        Default is Physical. Known values are: "Cash" and "Physical".
    """

    end_date: "_models.Date" = rest_field(name="endDate")
    """The maturity date of the instrument. Possible values are: An adjustable date - requires a date
     expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g., '2021-01-01T00:00:00Z'). Or a
     relative adjustable date - requires a tenor expressed as a code indicating the period between
     the reference date (default reference date is the start date) and the end date of the
     instrument (e.g. '6M', '1Y'). Required."""
    start_date: Optional["_models.Date"] = rest_field(name="startDate")
    """The start date of the instrument. Possible values are: An adjustable date - requires a date
     expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g., '2021-01-01T00:00:00Z'). Or a
     relative adjustable date - requires a tenor expressed as a code indicating the period between
     the reference date (default reference date is the start date) and the end date of the
     instrument (e.g. '6M', '1Y'). Default is the spot date."""
    settlement_type: Optional[Union[str, "_models.SettlementType"]] = rest_field(name="settlementType")
    """How the instrument is settled.  Possible values are: Physical or Cash. Default is Physical.
     Known values are: \"Cash\" and \"Physical\"."""

    @overload
    def __init__(
        self,
        *,
        fx_rate: "_models.FxRate",
        end_date: "_models.Date",
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
        start_date: Optional["_models.Date"] = None,
        settlement_type: Optional[Union[str, "_models.SettlementType"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardInvalidConstituent(FxInvalidConstituent, discriminator="FxForward"):
    """FxForwardInvalidConstituent.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.FX_FORWARD
        The type of constituent.  FxForward is the only valid value. Required.
    definition : ~analyticsapi.models.FxForwardConstituentDefinition
        An object to define the FX forward instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_FORWARD] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxForward is the only valid value. Required."""
    definition: Optional["_models.FxForwardConstituentDefinition"] = rest_field()
    """An object to define the FX forward instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.FxForwardConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_FORWARD, **kwargs)


class FxForwardOnTheFlyPriceResponse(_model_base.Model):
    """FxForwardOnTheFlyPriceResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardOnTheFlyPricingContext
    data : ~analyticsapi.models.FxForwardAnalyticsPricing
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxForwardOnTheFlyPricingContext"] = rest_field()
    data: Optional["_models.FxForwardAnalyticsPricing"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardOnTheFlyPricingContext"] = None,
        data: Optional["_models.FxForwardAnalyticsPricing"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardOnTheFlyPricingContext(_model_base.Model):
    """FxForwardOnTheFlyPricingContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD
    definition : ~analyticsapi.models.FxForwardInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_FORWARD]] = rest_field(visibility=["read"], default=ResourceType.FX_FORWARD)
    definition: "_models.FxForwardInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        definition: "_models.FxForwardInstrument",
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardOnTheFlyValuationContext(_model_base.Model):
    """FxForwardOnTheFlyValuationContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD
    definition : ~analyticsapi.models.FxForwardInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_FORWARD]] = rest_field(visibility=["read"], default=ResourceType.FX_FORWARD)
    definition: "_models.FxForwardInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        definition: "_models.FxForwardInstrument",
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardOnTheFlyValuationResponse(_model_base.Model):
    """FxForwardOnTheFlyValuationResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardOnTheFlyValuationContext
    data : ~analyticsapi.models.FxForwardAnalyticsValuation
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxForwardOnTheFlyValuationContext"] = rest_field()
    data: Optional["_models.FxForwardAnalyticsValuation"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardOnTheFlyValuationContext"] = None,
        data: Optional["_models.FxForwardAnalyticsValuation"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardPriceResponse(_model_base.Model):
    """FxForwardPriceResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardOnTheFlyPricingContext
    data : ~analyticsapi.models.FxForwardAnalyticsPricing
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxForwardOnTheFlyPricingContext"] = rest_field()
    data: Optional["_models.FxForwardAnalyticsPricing"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardOnTheFlyPricingContext"] = None,
        data: Optional["_models.FxForwardAnalyticsPricing"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxPricingAnalysis(_model_base.Model):
    """The analytics fields that are linked to a pre-trade analysis of the instrument.

    Attributes
    ----------
    fx_spot : ~analyticsapi.models.BidAskSimpleValues
        The spot price for the currency pair. The field returns the following
        values: Bid (Bid value), Ask (Ask value), Mid (Mid value).
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the amount of
        the deal (base) currency.
    """

    fx_spot: Optional["_models.BidAskSimpleValues"] = rest_field(name="fxSpot")
    """The spot price for the currency pair. The field returns the following values: Bid (Bid value),
     Ask (Ask value), Mid (Mid value)."""
    deal_amount: Optional[float] = rest_field(name="dealAmount")
    """The amount of the deal (base) currency bought or sold."""
    contra_amount: Optional[float] = rest_field(name="contraAmount")
    """The amount of contra currency exchanged to buy or sell the amount of the deal (base) currency."""

    @overload
    def __init__(
        self,
        *,
        fx_spot: Optional["_models.BidAskSimpleValues"] = None,
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardPricingAnalysis(FxPricingAnalysis):
    """The analytic fields that are linked to a pre-trade analysis of the instrument.

    Attributes
    ----------
    fx_spot : ~analyticsapi.models.BidAskSimpleValues
        The spot price for the currency pair. The field returns the following
        values: Bid (Bid value), Ask (Ask value), Mid (Mid value).
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the amount of
        the deal (base) currency.
    fx_swaps_ccy1 : ~analyticsapi.models.BidAskSimpleValues
        FX Swap points for the currency 1 against the reference currency. By
        default, the reference currency is USD.
    fx_swaps_ccy2 : ~analyticsapi.models.BidAskSimpleValues
        FX Swap points for the currency 2 against the reference currency. By
        default, the reference currency is USD.
    fx_swaps_ccy1_ccy2 : ~analyticsapi.models.BidAskSimpleValues
        FX Swap points for the FX cross currency pair.
    fx_outright_ccy1_ccy2 : ~analyticsapi.models.BidAskSimpleValues
        FX outright forward points for the FX cross currency pair.
    traded_cross_rate : float
        The contractual exchange rate agreed by the parties. Required.
    settlement_amount : float
        The settlement amount in an Fx Non-Deliverable Forward (NDF) contract.
        The value is expressed in the settlement currency.
    """

    fx_swaps_ccy1: Optional["_models.BidAskSimpleValues"] = rest_field(name="fxSwapsCcy1")
    """FX Swap points for the currency 1 against the reference currency. By default, the reference
     currency is USD."""
    fx_swaps_ccy2: Optional["_models.BidAskSimpleValues"] = rest_field(name="fxSwapsCcy2")
    """FX Swap points for the currency 2 against the reference currency. By default, the reference
     currency is USD."""
    fx_swaps_ccy1_ccy2: Optional["_models.BidAskSimpleValues"] = rest_field(name="fxSwapsCcy1Ccy2")
    """FX Swap points for the FX cross currency pair."""
    fx_outright_ccy1_ccy2: Optional["_models.BidAskSimpleValues"] = rest_field(name="fxOutrightCcy1Ccy2")
    """FX outright forward points for the FX cross currency pair."""
    traded_cross_rate: float = rest_field(name="tradedCrossRate")
    """The contractual exchange rate agreed by the parties. Required."""
    settlement_amount: Optional[float] = rest_field(name="settlementAmount")
    """The settlement amount in an Fx Non-Deliverable Forward (NDF) contract. The value is expressed
     in the settlement currency."""

    @overload
    def __init__(
        self,
        *,
        traded_cross_rate: float,
        fx_spot: Optional["_models.BidAskSimpleValues"] = None,
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
        fx_swaps_ccy1: Optional["_models.BidAskSimpleValues"] = None,
        fx_swaps_ccy2: Optional["_models.BidAskSimpleValues"] = None,
        fx_swaps_ccy1_ccy2: Optional["_models.BidAskSimpleValues"] = None,
        fx_outright_ccy1_ccy2: Optional["_models.BidAskSimpleValues"] = None,
        settlement_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardResource(_model_base.Model):
    """An object describing the basic properties of a resource on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_FORWARD
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxForwardInstrument
        Required.
    """

    type: Optional[Literal[ResourceType.FX_FORWARD]] = rest_field(visibility=["read"], default=ResourceType.FX_FORWARD)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxForwardInstrument" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxForwardInstrument",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardResponse(_model_base.Model):
    """FxForwardResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.FxForwardResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.FxForwardResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.FxForwardResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxRisk(_model_base.Model):
    """The analytics fields that are linked to a risk analysis of the instrument.

    Attributes
    ----------
    delta_percent : float
        The percentage change in the instrument's price or market value caused
        by a one-unit change in the price of the underlying asset, or by a 1bp
        change in the swap rate for a swaption, or by a 100bp change in the
        outright for a FX instrument.
    delta_amount_in_deal_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the deal currency.
    delta_amount_in_contra_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the contra (quote) currency.
    delta_amount_in_report_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the reporting currency.
    """

    delta_percent: Optional[float] = rest_field(name="deltaPercent")
    """The percentage change in the instrument's price or market value caused by a one-unit change in
     the price of the underlying asset, or by a 1bp change in the swap rate for a swaption, or by a
     100bp change in the outright for a FX instrument."""
    delta_amount_in_deal_ccy: Optional[float] = rest_field(name="deltaAmountInDealCcy")
    """The change in the instrument's price or market value caused by a one-unit change in the price
     of the underlying asset, or by a 1bp change in the swap rate for a swaption, or by a 100bp
     change in the outright for a FX instrument. The value is expressed in the deal currency."""
    delta_amount_in_contra_ccy: Optional[float] = rest_field(name="deltaAmountInContraCcy")
    """The change in the instrument's price or market value caused by a one-unit change in the price
     of the underlying asset, or by a 1bp change in the swap rate for a swaption, or by a 100bp
     change in the outright for a FX instrument. The value is expressed in the contra (quote)
     currency."""
    delta_amount_in_report_ccy: Optional[float] = rest_field(name="deltaAmountInReportCcy")
    """The change in the instrument's price or market value caused by a one-unit change in the price
     of the underlying asset, or by a 1bp change in the swap rate for a swaption, or by a 100bp
     change in the outright for a FX instrument. The value is expressed in the reporting currency."""

    @overload
    def __init__(
        self,
        *,
        delta_percent: Optional[float] = None,
        delta_amount_in_deal_ccy: Optional[float] = None,
        delta_amount_in_contra_ccy: Optional[float] = None,
        delta_amount_in_report_ccy: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardRisk(FxRisk):
    """The analytic fields that are linked to a risk analysis of the instrument.

    Attributes
    ----------
    delta_percent : float
        The percentage change in the instrument's price or market value caused
        by a one-unit change in the price of the underlying asset, or by a 1bp
        change in the swap rate for a swaption, or by a 100bp change in the
        outright for a FX instrument.
    delta_amount_in_deal_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the deal currency.
    delta_amount_in_contra_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the contra (quote) currency.
    delta_amount_in_report_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the reporting currency.
    """

    @overload
    def __init__(
        self,
        *,
        delta_percent: Optional[float] = None,
        delta_amount_in_deal_ccy: Optional[float] = None,
        delta_amount_in_contra_ccy: Optional[float] = None,
        delta_amount_in_report_ccy: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxValuation(_model_base.Model):
    """The analytics fields that are linked to a post-trade analysis of the instrument.

    Attributes
    ----------
    market_value_in_deal_ccy : float
        The market value of the instrument in the deal currency.
    market_value_in_contra_ccy : float
        The market value of the instrument in the contra (quote) currency.
    market_value_in_report_ccy : float
        The present value of the future cash flow in the reporting currency.
    """

    market_value_in_deal_ccy: Optional[float] = rest_field(name="marketValueInDealCcy")
    """The market value of the instrument in the deal currency."""
    market_value_in_contra_ccy: Optional[float] = rest_field(name="marketValueInContraCcy")
    """The market value of the instrument in the contra (quote) currency."""
    market_value_in_report_ccy: Optional[float] = rest_field(name="marketValueInReportCcy")
    """The present value of the future cash flow in the reporting currency."""

    @overload
    def __init__(
        self,
        *,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_contra_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxForwardValuation(FxValuation):
    """FxForwardValuation.

    Attributes
    ----------
    market_value_in_deal_ccy : float
        The market value of the instrument in the deal currency.
    market_value_in_contra_ccy : float
        The market value of the instrument in the contra (quote) currency.
    market_value_in_report_ccy : float
        The present value of the future cash flow in the reporting currency.
    discount_factor : float
        The ratio derived from the EndDate and used to calculate the present
        value of future cash flow for the instrument at MarketDataDate.
    """

    discount_factor: Optional[float] = rest_field(name="discountFactor")
    """The ratio derived from the EndDate and used to calculate the present value of future cash flow
     for the instrument at MarketDataDate."""

    @overload
    def __init__(
        self,
        *,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_contra_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
        discount_factor: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["discount_factor"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class FxForwardValuationResponse(_model_base.Model):
    """FxForwardValuationResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxForwardOnTheFlyValuationContext
    data : ~analyticsapi.models.FxForwardAnalyticsValuation
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxForwardOnTheFlyValuationContext"] = rest_field()
    data: Optional["_models.FxForwardAnalyticsValuation"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxForwardOnTheFlyValuationContext"] = None,
        data: Optional["_models.FxForwardAnalyticsValuation"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxPricingPreferences(_model_base.Model):
    """Object describing fx calculation parameters.

    Attributes
    ----------
    ignore_reference_currency_holidays : bool
        Set to True to ignore reference currency holidays.
    reference_currency : ~analyticsapi.models.CurrencyInput
        An object to specify the reference currency.
    report_currency : ~analyticsapi.models.CurrencyInput
        An object to specify the reporting currency.
    """

    ignore_reference_currency_holidays: Optional[bool] = rest_field(name="ignoreReferenceCurrencyHolidays")
    """Set to True to ignore reference currency holidays."""
    reference_currency: Optional["_models.CurrencyInput"] = rest_field(name="referenceCurrency")
    """An object to specify the reference currency."""
    report_currency: Optional["_models.CurrencyInput"] = rest_field(name="reportCurrency")
    """An object to specify the reporting currency."""

    @overload
    def __init__(
        self,
        *,
        ignore_reference_currency_holidays: Optional[bool] = None,
        reference_currency: Optional["_models.CurrencyInput"] = None,
        report_currency: Optional["_models.CurrencyInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxRate(_model_base.Model):
    """Definition of a FX rate.

    Attributes
    ----------
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The cross currency pair expressed in ISO 4217 alphabetical format (e.g.
        'EURCHF'). Required.
    rate : float
        The contractual exchange rate agreed by the parties. This is used to
        compute the contra amount if it is not provided.
    """

    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The cross currency pair expressed in ISO 4217 alphabetical format (e.g. 'EURCHF'). Required."""
    rate: Optional[float] = rest_field()
    """The contractual exchange rate agreed by the parties. This is used to compute the contra amount
     if it is not provided."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        rate: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotAnalyticsDescription(FxAnalyticsDescription):
    """The analytic fields that describe the instrument.

    Attributes
    ----------
    valuation_date : ~datetime.date
        The date at which the instrument is valued. The date is expressed in
        ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        '2021-01-01T00:00:00Z').
    start_date : ~analyticsapi.models.AdjustedDate
        The start date of the instrument.
    end_date : ~analyticsapi.models.AdjustedDate
        The maturity date of the instrument.
    """

    @overload
    def __init__(
        self,
        *,
        valuation_date: Optional[datetime.date] = None,
        start_date: Optional["_models.AdjustedDate"] = None,
        end_date: Optional["_models.AdjustedDate"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotAnalyticsPricing(_model_base.Model):
    """Object defining output of Fx Spot pricing analysis.

    Attributes
    ----------
    description : ~analyticsapi.models.FxSpotAnalyticsDescription
        The analytic fields that describe the instrument.
    pricing_analysis : ~analyticsapi.models.FxSpotPricingAnalysis
        The analytic fields that are linked to a pre-trade analysis of the
        instrument.
    greeks : ~analyticsapi.models.FxSpotRisk
        The analytic fields that are linked to a risk analysis of the
        instrument.
    processing_information : list[str]
    """

    description: Optional["_models.FxSpotAnalyticsDescription"] = rest_field()
    """The analytic fields that describe the instrument."""
    pricing_analysis: Optional["_models.FxSpotPricingAnalysis"] = rest_field(name="pricingAnalysis")
    """The analytic fields that are linked to a pre-trade analysis of the instrument."""
    greeks: Optional["_models.FxSpotRisk"] = rest_field()
    """The analytic fields that are linked to a risk analysis of the instrument."""
    processing_information: Optional[List[str]] = rest_field(name="processingInformation")

    @overload
    def __init__(
        self,
        *,
        description: Optional["_models.FxSpotAnalyticsDescription"] = None,
        pricing_analysis: Optional["_models.FxSpotPricingAnalysis"] = None,
        greeks: Optional["_models.FxSpotRisk"] = None,
        processing_information: Optional[List[str]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.processing_information is None:
            self.processing_information = list()


class FxSpotAnalyticsValuation(_model_base.Model):
    """Object defining output of Fx Spot valuation analysis.

    Attributes
    ----------
    description : ~analyticsapi.models.FxSpotAnalyticsDescription
        The analytic fields that describe the instrument.
    valuation : ~analyticsapi.models.FxSpotValuation
        The analytic fields that are linked to a post-trade analysis of the
        instrument.
    greeks : ~analyticsapi.models.FxSpotRisk
        The analytic fields that are linked to a risk analysis of the
        instrument.
    processing_information : list[str]
    """

    description: Optional["_models.FxSpotAnalyticsDescription"] = rest_field()
    """The analytic fields that describe the instrument."""
    valuation: Optional["_models.FxSpotValuation"] = rest_field()
    """The analytic fields that are linked to a post-trade analysis of the instrument."""
    greeks: Optional["_models.FxSpotRisk"] = rest_field()
    """The analytic fields that are linked to a risk analysis of the instrument."""
    processing_information: Optional[List[str]] = rest_field(name="processingInformation")

    @overload
    def __init__(
        self,
        *,
        description: Optional["_models.FxSpotAnalyticsDescription"] = None,
        valuation: Optional["_models.FxSpotValuation"] = None,
        greeks: Optional["_models.FxSpotRisk"] = None,
        processing_information: Optional[List[str]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.processing_information is None:
            self.processing_information = list()


class FxSpotAsCollectionItem(_model_base.Model):
    """An object describing the basic properties of an FX spot.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotCollectionLinks(_model_base.Model):
    """FxSpotCollectionLinks.

    Attributes
    ----------
    self_property : ~analyticsapi.models.Link
        Required.
    first : ~analyticsapi.models.Link
    prev : ~analyticsapi.models.Link
    next : ~analyticsapi.models.Link
    last : ~analyticsapi.models.Link
    price : ~analyticsapi.models.Link
        Required.
    value : ~analyticsapi.models.Link
        Required.
    """

    self_property: "_models.Link" = rest_field(name="self")
    """Required."""
    first: Optional["_models.Link"] = rest_field()
    prev: Optional["_models.Link"] = rest_field()
    next: Optional["_models.Link"] = rest_field()
    last: Optional["_models.Link"] = rest_field()
    price: "_models.Link" = rest_field()
    """Required."""
    value: "_models.Link" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        self_property: "_models.Link",
        price: "_models.Link",
        value: "_models.Link",
        first: Optional["_models.Link"] = None,
        prev: Optional["_models.Link"] = None,
        next: Optional["_models.Link"] = None,
        last: Optional["_models.Link"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotCollectionResponse(_model_base.Model):
    """FxSpotCollectionResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.FxSpotAsCollectionItem]
        Required.
    links : ~analyticsapi.models.FxSpotCollectionLinks
    """

    data: List["_models.FxSpotAsCollectionItem"] = rest_field()
    """Required."""
    links: Optional["_models.FxSpotCollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.FxSpotAsCollectionItem"],
        links: Optional["_models.FxSpotCollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class FxSpotConstituent(FxForwardCurveConstituent, discriminator="FxSpot"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    quote : ~analyticsapi.models.QuoteInput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    type : str or ~analyticsapi.models.FX_SPOT
        The type of constituent.  FxSpot is the only valid value. Required.
    definition : ~analyticsapi.models.FxSpotConstituentDefinition
        An object to define the FX spot instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_SPOT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxSpot is the only valid value. Required."""
    definition: Optional["_models.FxSpotConstituentDefinition"] = rest_field()
    """An object to define the FX spot instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        quote: Optional["_models.QuoteInput"] = None,
        definition: Optional["_models.FxSpotConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_SPOT, **kwargs)


class FxSpotConstituentDefinition(_model_base.Model):
    """An object to define the FX spot instrument used as a constituent.

    Attributes
    ----------
    tenor : str
        A tenor (relatvie date) expressed as a code, indicating the period
        covered by the constituent.
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    """

    tenor: Optional[str] = rest_field()
    """A tenor (relatvie date) expressed as a code, indicating the period covered by the constituent."""
    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The currency pair, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF'). Required."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        tenor: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotConstituentValues(FxForwardCurveConstituentValues, discriminator="FxSpot"):
    """An object to define constituents that are used to construct the curve.

    Attributes
    ----------
    quote : ~analyticsapi.models.QuoteOutput
        An object to define the quote of the instrument used as a constituent.
        Optional: provide either a definition or a quote.
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.FX_SPOT
        The type of constituent.  FxSpot is the only valid value. Required.
    definition : ~analyticsapi.models.FxSpotConstituentDefinition
        An object to define the FX spot instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_SPOT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxSpot is the only valid value. Required."""
    definition: Optional["_models.FxSpotConstituentDefinition"] = rest_field()
    """An object to define the FX spot instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        quote: Optional["_models.QuoteOutput"] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.FxSpotConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_SPOT, **kwargs)


class FxSpotDefinition(FxPayment):
    """The definition of the Fx spot.

    Attributes
    ----------
    fx_rate : ~analyticsapi.models.FxRate
        An object defining the FX rate. Required.
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the deal (base)
        currency.
    """

    @overload
    def __init__(
        self,
        *,
        fx_rate: "_models.FxRate",
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotInstrument(FxSpotDefinition):
    """The definition of the Fx spot instument.

    Attributes
    ----------
    fx_rate : ~analyticsapi.models.FxRate
        An object defining the FX rate. Required.
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the deal (base)
        currency.
    """

    @overload
    def __init__(
        self,
        *,
        fx_rate: "_models.FxRate",
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotInvalidConstituent(FxInvalidConstituent, discriminator="FxSpot"):
    """FxSpotInvalidConstituent.

    Attributes
    ----------
    source : str
        The code of the contributor of the quote for the instrument used as a
        constituent (e.g., 'ICAP').
    status_message : str
        The status of the constituent.
    type : str or ~analyticsapi.models.FX_SPOT
        The type of constituent.  FxSpot is the only valid value. Required.
    definition : ~analyticsapi.models.FxSpotConstituentDefinition
        An object to define the FX spot instrument used as a constituent.
    """

    type: Literal[FxForwardCurveConstituentType.FX_SPOT] = rest_discriminator(name="type")  # type: ignore
    """The type of constituent.  FxSpot is the only valid value. Required."""
    definition: Optional["_models.FxSpotConstituentDefinition"] = rest_field()
    """An object to define the FX spot instrument used as a constituent."""

    @overload
    def __init__(
        self,
        *,
        source: Optional[str] = None,
        status_message: Optional[str] = None,
        definition: Optional["_models.FxSpotConstituentDefinition"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, type=FxForwardCurveConstituentType.FX_SPOT, **kwargs)


class FxSpotOnTheFlyPriceResponse(_model_base.Model):
    """FxSpotOnTheFlyPriceResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxSpotOnTheFlyPricingContext
    data : ~analyticsapi.models.FxSpotAnalyticsPricing
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxSpotOnTheFlyPricingContext"] = rest_field()
    data: Optional["_models.FxSpotAnalyticsPricing"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxSpotOnTheFlyPricingContext"] = None,
        data: Optional["_models.FxSpotAnalyticsPricing"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotOnTheFlyPricingContext(_model_base.Model):
    """FxSpotOnTheFlyPricingContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
    definition : ~analyticsapi.models.FxSpotInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    definition: "_models.FxSpotInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        definition: "_models.FxSpotInstrument",
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotOnTheFlyValuationContext(_model_base.Model):
    """FxSpotOnTheFlyValuationContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
    definition : ~analyticsapi.models.FxSpotInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    definition: "_models.FxSpotInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        definition: "_models.FxSpotInstrument",
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotOnTheFlyValuationResponse(_model_base.Model):
    """FxSpotOnTheFlyValuationResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxSpotOnTheFlyValuationContext
    data : ~analyticsapi.models.FxSpotAnalyticsValuation
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxSpotOnTheFlyValuationContext"] = rest_field()
    data: Optional["_models.FxSpotAnalyticsValuation"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxSpotOnTheFlyValuationContext"] = None,
        data: Optional["_models.FxSpotAnalyticsValuation"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotPriceResponse(_model_base.Model):
    """FxSpotPriceResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxSpotPricingContext
    data : ~analyticsapi.models.FxSpotAnalyticsPricing
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxSpotPricingContext"] = rest_field()
    data: Optional["_models.FxSpotAnalyticsPricing"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxSpotPricingContext"] = None,
        data: Optional["_models.FxSpotAnalyticsPricing"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotPricingAnalysis(FxPricingAnalysis):
    """The analytic fields that are linked to a pre-trade analysis of the instrument.

    Attributes
    ----------
    fx_spot : ~analyticsapi.models.BidAskSimpleValues
        The spot price for the currency pair. The field returns the following
        values: Bid (Bid value), Ask (Ask value), Mid (Mid value).
    deal_amount : float
        The amount of the deal (base) currency bought or sold.
    contra_amount : float
        The amount of contra currency exchanged to buy or sell the amount of
        the deal (base) currency.
    """

    @overload
    def __init__(
        self,
        *,
        fx_spot: Optional["_models.BidAskSimpleValues"] = None,
        deal_amount: Optional[float] = None,
        contra_amount: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotPricingContext(_model_base.Model):
    """FxSpotPricingContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxSpotInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxSpotInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxSpotInstrument",
        description: Optional["_models.Description"] = None,
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotResource(_model_base.Model):
    """An object describing the basic properties of a resource on the platform.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxSpotInstrument
        Required.
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxSpotInstrument" = rest_field()
    """Required."""

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxSpotInstrument",
        description: Optional["_models.Description"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotResponse(_model_base.Model):
    """FxSpotResponse.

    Attributes
    ----------
    data : ~analyticsapi.models.FxSpotResource
        Required.
    meta : ~analyticsapi.models.MetaData
    """

    data: "_models.FxSpotResource" = rest_field()
    """Required."""
    meta: Optional["_models.MetaData"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: "_models.FxSpotResource",
        meta: Optional["_models.MetaData"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotRisk(FxRisk):
    """The analytic fields that are linked to a risk analysis of the instrument.

    Attributes
    ----------
    delta_percent : float
        The percentage change in the instrument's price or market value caused
        by a one-unit change in the price of the underlying asset, or by a 1bp
        change in the swap rate for a swaption, or by a 100bp change in the
        outright for a FX instrument.
    delta_amount_in_deal_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the deal currency.
    delta_amount_in_contra_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the contra (quote) currency.
    delta_amount_in_report_ccy : float
        The change in the instrument's price or market value caused by a one-
        unit change in the price of the underlying asset, or by a 1bp change in
        the swap rate for a swaption, or by a 100bp change in the outright for
        a FX instrument. The value is expressed in the reporting currency.
    """

    @overload
    def __init__(
        self,
        *,
        delta_percent: Optional[float] = None,
        delta_amount_in_deal_ccy: Optional[float] = None,
        delta_amount_in_contra_ccy: Optional[float] = None,
        delta_amount_in_report_ccy: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotValuation(FxValuation):
    """The analytic fields that are linked to a post-trade analysis of the instrument.

    Attributes
    ----------
    market_value_in_deal_ccy : float
        The market value of the instrument in the deal currency.
    market_value_in_contra_ccy : float
        The market value of the instrument in the contra (quote) currency.
    market_value_in_report_ccy : float
        The present value of the future cash flow in the reporting currency.
    """

    @overload
    def __init__(
        self,
        *,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_contra_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotValuationContext(_model_base.Model):
    """FxSpotValuationContext.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    type : str or ~analyticsapi.models.FX_SPOT
        The resource type. Possible values are: Calendar, Currency,
        CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot,
        NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str
        Unique resource ID specified by LSEG.
    location : ~analyticsapi.models.Location
        Location of the platform where resource is stored. Required.
    description : ~analyticsapi.models.Description
        Description object that contains the resource summary and tags.
    definition : ~analyticsapi.models.FxSpotInstrument
        Required.
    parameters : ~analyticsapi.models.PricingParameters
    market_data : ~analyticsapi.models.MarketDataInput
    """

    type: Optional[Literal[ResourceType.FX_SPOT]] = rest_field(visibility=["read"], default=ResourceType.FX_SPOT)
    """The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve,
     FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or
     Space."""
    id: Optional[str] = rest_field(visibility=["read"])
    """Unique resource ID specified by LSEG."""
    location: "_models.Location" = rest_field()
    """Location of the platform where resource is stored. Required."""
    description: Optional["_models.Description"] = rest_field()
    """Description object that contains the resource summary and tags."""
    definition: "_models.FxSpotInstrument" = rest_field()
    """Required."""
    parameters: Optional["_models.PricingParameters"] = rest_field()
    market_data: Optional["_models.MarketDataInput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        location: "_models.Location",
        definition: "_models.FxSpotInstrument",
        description: Optional["_models.Description"] = None,
        parameters: Optional["_models.PricingParameters"] = None,
        market_data: Optional["_models.MarketDataInput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxSpotValuationResponse(_model_base.Model):
    """FxSpotValuationResponse.

    Attributes
    ----------
    context : ~analyticsapi.models.FxSpotValuationContext
    data : ~analyticsapi.models.FxSpotAnalyticsValuation
    market_data : ~analyticsapi.models.MarketDataOutput
    """

    context: Optional["_models.FxSpotValuationContext"] = rest_field()
    data: Optional["_models.FxSpotAnalyticsValuation"] = rest_field()
    market_data: Optional["_models.MarketDataOutput"] = rest_field(name="marketData")

    @overload
    def __init__(
        self,
        *,
        context: Optional["_models.FxSpotValuationContext"] = None,
        data: Optional["_models.FxSpotAnalyticsValuation"] = None,
        market_data: Optional["_models.MarketDataOutput"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class FxUnderlyingCurve(_model_base.Model):
    """FxUnderlyingCurve.

    Attributes
    ----------
    cross_currency : ~analyticsapi.models.CrossCurrencyInput
        The currency pair, expressed in ISO 4217 alphabetical format (e.g.,
        'EURCHF'). Required.
    curve_points : list[~analyticsapi.models.FxForwardCurvePoint]
        An array of objects that contains curve points and related attributes
        of the underlying curve.
    """

    cross_currency: "_models.CrossCurrencyInput" = rest_field(name="crossCurrency")
    """The currency pair, expressed in ISO 4217 alphabetical format (e.g., 'EURCHF'). Required."""
    curve_points: Optional[List["_models.FxForwardCurvePoint"]] = rest_field(name="curvePoints")
    """An array of objects that contains curve points and related attributes of the underlying curve."""

    @overload
    def __init__(
        self,
        *,
        cross_currency: "_models.CrossCurrencyInput",
        curve_points: Optional[List["_models.FxForwardCurvePoint"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.curve_points is None:
            self.curve_points = list()


class GenerateDateScheduleResponse(_model_base.Model):
    """GenerateDateScheduleResponse.

    Attributes
    ----------
    data : list[~datetime.date]
        Required.
    links : ~analyticsapi.models.CollectionLinks
    """

    data: List[datetime.date] = rest_field()
    """Required."""
    links: Optional["_models.CollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List[datetime.date],
        links: Optional["_models.CollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class GenerateHolidaysResponse(_model_base.Model):
    """GenerateHolidaysResponse.

    Attributes
    ----------
    data : list[~analyticsapi.models.HolidayOutput]
        Required.
    links : ~analyticsapi.models.CollectionLinks
    """

    data: List["_models.HolidayOutput"] = rest_field()
    """Required."""
    links: Optional["_models.CollectionLinks"] = rest_field()

    @overload
    def __init__(
        self,
        *,
        data: List["_models.HolidayOutput"],
        links: Optional["_models.CollectionLinks"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.data is None:
            self.data = list()


class HalfDayDuration(Duration, discriminator="HalfDayDuration"):
    """An object to determine the duration of the holiday within one day.

    Attributes
    ----------
    duration_type : str or ~analyticsapi.models.HALF_DAY_DURATION
        The type of the holiday duration. Only HalfDayDuration value applies.
        Required. Half day holidays. Designed to account for the days the
        markets are open, but not for a full trading session.
    start_time : ~analyticsapi.models.Time
        An object to determine the start time of the holiday duration.
    end_time : ~analyticsapi.models.Time
        An object to determine the end time of the holiday duration.
    """

    duration_type: Literal[DurationType.HALF_DAY_DURATION] = rest_discriminator(name="durationType")  # type: ignore
    """The type of the holiday duration. Only HalfDayDuration value applies. Required. Half day
     holidays. Designed to account for the days the markets are open, but not for a full trading
     session."""
    start_time: Optional["_models.Time"] = rest_field(name="startTime")
    """An object to determine the start time of the holiday duration."""
    end_time: Optional["_models.Time"] = rest_field(name="endTime")
    """An object to determine the end time of the holiday duration."""

    @overload
    def __init__(
        self,
        *,
        start_time: Optional["_models.Time"] = None,
        end_time: Optional["_models.Time"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, duration_type=DurationType.HALF_DAY_DURATION, **kwargs)


class HolidayOutput(_model_base.Model):
    """Dates and names of holidays for a requested calendar.

    Attributes
    ----------
    date : ~datetime.date
        The date on which the holiday falls. The value is expressed in ISO 8601
        format: YYYY-MM-DD (e.g., 2024-01-01). Required.
    names : list[~analyticsapi.models.HolidayOutputNames]
        An array of objects to define the holiday name, calendar and country in
        which the holiday falls.
    processing_information : str
        The error message for the calculation in case of a non-blocking error.
    """

    date: datetime.date = rest_field()
    """The date on which the holiday falls. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., 2024-01-01). Required."""
    names: Optional[List["_models.HolidayOutputNames"]] = rest_field()
    """An array of objects to define the holiday name, calendar and country in which the holiday
     falls."""
    processing_information: Optional[str] = rest_field(name="processingInformation")
    """The error message for the calculation in case of a non-blocking error."""

    @overload
    def __init__(
        self,
        *,
        date: datetime.date,
        names: Optional[List["_models.HolidayOutputNames"]] = None,
        processing_information: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.names is None:
            self.names = list()


class HolidayOutputNames(_model_base.Model):
    """An object to define the holiday name, calendar and country in which the holiday falls.

    Attributes
    ----------
    name : str
        The name of the holiday.
    calendars : list[~analyticsapi.models.CalendarRelatedResource]
        An array of calendar defining objects for which the calculation is
        done.
    countries : list[str]
        An array of country codes that the holiday belongs to. For example, FRA
        for France, UKG for The United Kingdom.
    """

    name: Optional[str] = rest_field()
    """The name of the holiday."""
    calendars: Optional[List["_models.CalendarRelatedResource"]] = rest_field()
    """An array of calendar defining objects for which the calculation is done."""
    countries: Optional[List[str]] = rest_field()
    """An array of country codes that the holiday belongs to. For example, FRA for France, UKG for The
     United Kingdom."""

    @overload
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        calendars: Optional[List["_models.CalendarRelatedResource"]] = None,
        countries: Optional[List[str]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.calendars is None:
            self.calendars = list()
        if self.countries is None:
            self.countries = list()


class HolidayRule(_model_base.Model):
    """A holiday rule for the calendar.

    Attributes
    ----------
    name : str
        The name of the holiday rule. Required.
    description : str
        The description of the holiday rule.
    duration : ~analyticsapi.models.Duration
        An object to specify the type of holiday. Either no trading or reduced
        trading. Required.
    validity_period : ~analyticsapi.models.ValidityPeriod
        An object to determine the start and end date of the holiday. Required.
    when : ~analyticsapi.models.When
        Object describing type of holiday rule. Possible values are:
        AbsolutePositionWhen (for fixed holidays), RelativePositionWhen (for
        holidays that fall on a particular day of the week) or
        RelativeToRulePositionWhen (for holidays that are set by reference to
        another date). Required.
    """

    name: str = rest_field()
    """The name of the holiday rule. Required."""
    description: Optional[str] = rest_field()
    """The description of the holiday rule."""
    duration: "_models.Duration" = rest_field()
    """An object to specify the type of holiday. Either no trading or reduced trading. Required."""
    validity_period: "_models.ValidityPeriod" = rest_field(name="validityPeriod")
    """An object to determine the start and end date of the holiday. Required."""
    when: "_models.When" = rest_field()
    """Object describing type of holiday rule. Possible values are: AbsolutePositionWhen (for fixed
     holidays), RelativePositionWhen (for holidays that fall on a particular day of the week) or
     RelativeToRulePositionWhen (for holidays that are set by reference to another date). Required."""

    @overload
    def __init__(
        self,
        *,
        name: str,
        duration: "_models.Duration",
        validity_period: "_models.ValidityPeriod",
        when: "_models.When",
        description: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class IndirectSourcesDeposits(_model_base.Model):
    """An object that defines the sources containing the market data for the deposit instruments used
    to create the curve definition.
    It applies when there is an indirect quotation for the currency pair of the curve.

    Attributes
    ----------
    base_fx_spot : str
        The source of FX spot for the base currency in the cross-currency pair
        of the curve against the reference currency.
    quoted_fx_spot : str
        The source of FX spot for the quoted currency in the cross-currency
        pair of the curve against the reference currency.
    base_deposit : str
        The source of deposits for the base currency in the cross-currency pair
        of the curve.
    quoted_deposit : str
        The source of deposits for the quoted currency in the cross-currency
        pair of the curve.
    """

    base_fx_spot: Optional[str] = rest_field(name="baseFxSpot")
    """The source of FX spot for the base currency in the cross-currency pair of the curve against the
     reference currency."""
    quoted_fx_spot: Optional[str] = rest_field(name="quotedFxSpot")
    """The source of FX spot for the quoted currency in the cross-currency pair of the curve against
     the reference currency."""
    base_deposit: Optional[str] = rest_field(name="baseDeposit")
    """The source of deposits for the base currency in the cross-currency pair of the curve."""
    quoted_deposit: Optional[str] = rest_field(name="quotedDeposit")
    """The source of deposits for the quoted currency in the cross-currency pair of the curve."""

    @overload
    def __init__(
        self,
        *,
        base_fx_spot: Optional[str] = None,
        quoted_fx_spot: Optional[str] = None,
        base_deposit: Optional[str] = None,
        quoted_deposit: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class IndirectSourcesSwaps(_model_base.Model):
    """An object that defines the sources containing the market data for the FX forward instruments
    used to create the curve definition.
    It applies when there is an indirect quotation for the currency pair of the curve.

    Attributes
    ----------
    base_fx_spot : str
        The source of FX spot for the base currency in the cross-currency pair.
    quoted_fx_spot : str
        The source of FX spot for the quoted currency in the cross-currency
        pair.
    base_fx_forwards : str
        The source of FX forwards for the base currency in the cross-currency
        pair.
    quoted_fx_forwards : str
        The source of FX forwards for the quoted currency in the cross-currency
        pair.
    """

    base_fx_spot: Optional[str] = rest_field(name="baseFxSpot")
    """The source of FX spot for the base currency in the cross-currency pair."""
    quoted_fx_spot: Optional[str] = rest_field(name="quotedFxSpot")
    """The source of FX spot for the quoted currency in the cross-currency pair."""
    base_fx_forwards: Optional[str] = rest_field(name="baseFxForwards")
    """The source of FX forwards for the base currency in the cross-currency pair."""
    quoted_fx_forwards: Optional[str] = rest_field(name="quotedFxForwards")
    """The source of FX forwards for the quoted currency in the cross-currency pair."""

    @overload
    def __init__(
        self,
        *,
        base_fx_spot: Optional[str] = None,
        quoted_fx_spot: Optional[str] = None,
        base_fx_forwards: Optional[str] = None,
        quoted_fx_forwards: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class InnerError(_model_base.Model):
    """An object that contains the detailed information in case of a blocking error in a calculation.

    Attributes
    ----------
    key : str
        The specification of the request in which an error occurs. Required.
    reason : str
        The reason why an error occurs. Required.
    name : str
        The name of the property causing the error.
    invalid_name : str
        The name of the invalid property.
    """

    key: str = rest_field()
    """The specification of the request in which an error occurs. Required."""
    reason: str = rest_field()
    """The reason why an error occurs. Required."""
    name: Optional[str] = rest_field()
    """The name of the property causing the error."""
    invalid_name: Optional[str] = rest_field(name="invalidName")
    """The name of the invalid property."""

    @overload
    def __init__(
        self,
        *,
        key: str,
        reason: str,
        name: Optional[str] = None,
        invalid_name: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class IrCurvePoint(_model_base.Model):
    """An object that contains the values applied to the interest rate curve point.

    Attributes
    ----------
    tenor : str
        A code indicating the length of the period between the start date and
        the end date of the curve point. Predefined values are: ON (Overnight -
        A one business day period that starts today), TN (Tomorrow-Next - A one
        business day period that starts next business day, SPOT (Spot Date), SN
        (Spot-Next - A one business day period that starts at the spot date of
        a currency pair) or SW (Spot-Week - A one business week period that
        starts at the spot date of a currency pair). Tenors can also be
        specified as a whole number of time units. Possible units are: D
        (Days), W (Weeks), M (Months) or Y (Years). For example, one month is
        written '1M', 3 years is written: '3Y'. Time units can be mixed. For
        example, 5M3D means '5 months and 3 days'. Note: units must be written
        in descending order of size (Y > M > W > D). Required.
    start_date : ~datetime.date
        The start date of the curve point tenor. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., '2023-01-01'). Required.
    end_date : ~datetime.date
        The end date of the curve point tenor. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., '2024-01-01'). Required.
    instruments : list[~analyticsapi.models.IrCurvePointRelatedInstruments]
        An array of objects that contains instruments used to calculate the
        curve point.
    rate_percent : ~analyticsapi.models.BidAskMidSimpleValues
        The rate percentage calculated for a given curve point. Required.
    discount_factor : float
        The discount factor calculated for a given curve point. Required.
    """

    tenor: str = rest_field()
    """A code indicating the length of the period between the start date and the end date of the curve
     point.
     Predefined values are: ON (Overnight - A one business day period that starts today), TN
     (Tomorrow-Next - A one business day period that starts next business day, SPOT (Spot Date), SN
     (Spot-Next - A one business day period that starts at the spot date of a currency pair) or SW
     (Spot-Week - A one business week period that starts at the spot date of a currency pair).
     Tenors can also be specified as a whole number of time units. Possible units are: D (Days), W
     (Weeks), M (Months) or Y (Years). For example, one month is written '1M', 3 years is written:
     '3Y'.
     Time units can be mixed. For example, 5M3D means '5 months and 3 days'. Note: units must be
     written in descending order of size (Y > M > W > D). Required."""
    start_date: datetime.date = rest_field(name="startDate")
    """The start date of the curve point tenor. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., '2023-01-01'). Required."""
    end_date: datetime.date = rest_field(name="endDate")
    """The end date of the curve point tenor. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., '2024-01-01'). Required."""
    instruments: Optional[List["_models.IrCurvePointRelatedInstruments"]] = rest_field()
    """An array of objects that contains instruments used to calculate the curve point."""
    rate_percent: "_models.BidAskMidSimpleValues" = rest_field(name="ratePercent")
    """The rate percentage calculated for a given curve point. Required."""
    discount_factor: float = rest_field(name="discountFactor")
    """The discount factor calculated for a given curve point. Required."""

    @overload
    def __init__(
        self,
        *,
        tenor: str,
        start_date: datetime.date,
        end_date: datetime.date,
        rate_percent: "_models.BidAskMidSimpleValues",
        discount_factor: float,
        instruments: Optional[List["_models.IrCurvePointRelatedInstruments"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instruments is None:
            self.instruments = list()


class IrCurvePointRelatedInstruments(_model_base.Model):
    """The instrument used to calculate the curve point.

    Attributes
    ----------
    instrument_code : str
        The identifier of the instrument used to calculate the curve point.
        Required.
    """

    instrument_code: str = rest_field(name="instrumentCode")
    """The identifier of the instrument used to calculate the curve point. Required."""

    @overload
    def __init__(
        self,
        instrument_code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["instrument_code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class IrUnderlyingCurve(_model_base.Model):
    """An object that contains the underlying interest rate curve used to construct the curve.

    Attributes
    ----------
    currency : ~analyticsapi.models.CurrencyInput
        The currency expressed in ISO 4217 alphabetical format (e.g., 'EUR').
        Required.
    curve_points : list[~analyticsapi.models.IrCurvePoint]
        An array of objects that contain the values applied to the interest
        rate curve points.
    """

    currency: "_models.CurrencyInput" = rest_field()
    """The currency expressed in ISO 4217 alphabetical format (e.g., 'EUR'). Required."""
    curve_points: Optional[List["_models.IrCurvePoint"]] = rest_field(name="curvePoints")
    """An array of objects that contain the values applied to the interest rate curve points."""

    @overload
    def __init__(
        self,
        *,
        currency: "_models.CurrencyInput",
        curve_points: Optional[List["_models.IrCurvePoint"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.curve_points is None:
            self.curve_points = list()


class RescheduleDescription(_model_base.Model):
    """An object to determine a holiday rescheduling.

    You probably want to use the sub-classes and not this class directly. Known sub-classes are:
    LagDaysRescheduleDescription, RelativeRescheduleDescription

    Attributes
    ----------
    reschedule_type : str or ~analyticsapi.models.RescheduleType
        The type of rescheduling for the observation period. Required. Known
        values are: "LagDaysRescheduleDescription" and
        "RelativeRescheduleDescription".
    """

    __mapping__: Dict[str, _model_base.Model] = {}
    reschedule_type: str = rest_discriminator(name="rescheduleType")
    """The type of rescheduling for the observation period. Required. Known values are:
     \"LagDaysRescheduleDescription\" and \"RelativeRescheduleDescription\"."""

    @overload
    def __init__(
        self,
        reschedule_type: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["reschedule_type"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class LagDaysRescheduleDescription(RescheduleDescription, discriminator="LagDaysRescheduleDescription"):
    """An object to define the rule for rescheduling a holiday using lag days.

    Attributes
    ----------
    reschedule_type : str or ~analyticsapi.models.LAG_DAYS_RESCHEDULE_DESCRIPTION
        The type of rescheduling for the observation period. Only
        LagDaysRescheduleDescription value applies. Required. Reschedule the
        holiday by specifying a lag period in days. For example, if a holiday
        falls on Sunday, it can be moved by one day so that it happens on the
        following Monday.
    lag_days : int
        The length of the lag in days. The holiday will be rescheduled to a
        date this many days in the future. Required.
    """

    reschedule_type: Literal[RescheduleType.LAG_DAYS_RESCHEDULE_DESCRIPTION] = rest_discriminator(name="rescheduleType")  # type: ignore
    """The type of rescheduling for the observation period. Only LagDaysRescheduleDescription value
     applies. Required. Reschedule the holiday by specifying a lag period in days. For example, if a
     holiday falls on Sunday, it can be moved by one day so that it happens on the following Monday."""
    lag_days: int = rest_field(name="lagDays")
    """The length of the lag in days. The holiday will be rescheduled to a date this many days in the
     future. Required."""

    @overload
    def __init__(
        self,
        lag_days: int,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, reschedule_type=RescheduleType.LAG_DAYS_RESCHEDULE_DESCRIPTION, **kwargs)


class Link(_model_base.Model):
    """Link.

    Attributes
    ----------
    href : str
        Required.
    href_schema : str
    http_method : str
    """

    href: str = rest_field()
    """Required."""
    href_schema: Optional[str] = rest_field(name="hrefSchema")
    http_method: Optional[str] = rest_field(name="httpMethod")

    @overload
    def __init__(
        self,
        *,
        href: str,
        href_schema: Optional[str] = None,
        http_method: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class Location(_model_base.Model):
    """An object to define a location in memory (space and name).

    Attributes
    ----------
    space : str
        The storage location for the resource.
    name : str
        The name of the resource. Required.
    """

    space: Optional[str] = rest_field()
    """The storage location for the resource."""
    name: str = rest_field()
    """The name of the resource. Required."""

    @overload
    def __init__(
        self,
        *,
        name: str,
        space: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class MarketDataInput(_model_base.Model):
    """An object defining market data to be used to compute the analytics.

    Attributes
    ----------
    fx_forward_curves : list[~analyticsapi.models.FxForwardCurveAsMarketDataInput]
        Object describing the FX forward curve used for the calculation. An
        array of FxForward curve inputs.
    """

    fx_forward_curves: Optional[List["_models.FxForwardCurveAsMarketDataInput"]] = rest_field(name="fxForwardCurves")
    """Object describing the FX forward curve used for the calculation. An array of FxForward curve
     inputs."""

    @overload
    def __init__(
        self,
        fx_forward_curves: Optional[List["_models.FxForwardCurveAsMarketDataInput"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["fx_forward_curves"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)
        if self.fx_forward_curves is None:
            self.fx_forward_curves = list()


class MarketDataOutput(_model_base.Model):
    """MarketDataOutput.

    Attributes
    ----------
    fx_forward_curves : list[~analyticsapi.models.FxForwardCurveAsMarketDataOutput]
    """

    fx_forward_curves: Optional[List["_models.FxForwardCurveAsMarketDataOutput"]] = rest_field(name="fxForwardCurves")

    @overload
    def __init__(
        self,
        fx_forward_curves: Optional[List["_models.FxForwardCurveAsMarketDataOutput"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["fx_forward_curves"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)
        if self.fx_forward_curves is None:
            self.fx_forward_curves = list()


class MetaData(_model_base.Model):
    """The metadata of the resource.Metadata properites.

    Attributes
    ----------
    create_time : ~datetime.datetime
        The date and time when the resource was created. The value is expressed
        in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        2023-01-01T00:00:00Z). Required.
    status : str or ~analyticsapi.models.Status
        The status of the resource. Required. Known values are: "Active" and
        "Deleted".
    revision : str
        The version of the resource. Required.
    creator : str
        The uuid of the user who created the resource. Required.
    update_time : ~datetime.datetime
        The date and time when the resource was updated. The value is expressed
        in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        2023-01-01T00:00:00Z).
    delete_time : ~datetime.datetime
        The date and time when the resource was deleted. The value is expressed
        in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
        2023-01-01T00:00:00Z).
    updated_by : str
        The name of the user who updated the resource.
    """

    create_time: datetime.datetime = rest_field(name="createTime", format="rfc3339")
    """The date and time when the resource was created.
     The value is expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
     2023-01-01T00:00:00Z). Required."""
    status: Union[str, "_models.Status"] = rest_field()
    """The status of the resource. Required. Known values are: \"Active\" and \"Deleted\"."""
    revision: str = rest_field()
    """The version of the resource. Required."""
    creator: str = rest_field()
    """The uuid of the user who created the resource. Required."""
    update_time: Optional[datetime.datetime] = rest_field(name="updateTime", format="rfc3339")
    """The date and time when the resource was updated.
     The value is expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
     2023-01-01T00:00:00Z)."""
    delete_time: Optional[datetime.datetime] = rest_field(name="deleteTime", format="rfc3339")
    """The date and time when the resource was deleted.
     The value is expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g.,
     2023-01-01T00:00:00Z)."""
    updated_by: Optional[str] = rest_field(name="updatedBy")
    """The name of the user who updated the resource."""

    @overload
    def __init__(
        self,
        *,
        create_time: datetime.datetime,
        status: Union[str, "_models.Status"],
        revision: str,
        creator: str,
        update_time: Optional[datetime.datetime] = None,
        delete_time: Optional[datetime.datetime] = None,
        updated_by: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class Observance(_model_base.Model):
    """An object to determine how a holiday is rescheduled if it falls on a rest day.

    Attributes
    ----------
    falls_on : str or ~analyticsapi.models.WeekDay
        The day of the week that the holiday falls on. This is used as a
        reference point. Required. Known values are: "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Saturday", and "Sunday".
    reschedule_description : ~analyticsapi.models.RescheduleDescription
        An object to determine a holiday rescheduling. Required.
    """

    falls_on: Union[str, "_models.WeekDay"] = rest_field(name="fallsOn")
    """The day of the week that the holiday falls on. This is used as a reference point. Required.
     Known values are: \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\",
     \"Saturday\", and \"Sunday\"."""
    reschedule_description: "_models.RescheduleDescription" = rest_field(name="rescheduleDescription")
    """An object to determine a holiday rescheduling. Required."""

    @overload
    def __init__(
        self,
        *,
        falls_on: Union[str, "_models.WeekDay"],
        reschedule_description: "_models.RescheduleDescription",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class PricingParameters(_model_base.Model):
    """Base cross asset calculation parameters.

    Attributes
    ----------
    valuation_date : ~datetime.date
        The date at which the instrument is valued. The value is expressed in
        ISO 8601 format: YYYY-MM-DD (e.g., '2021-01-01'). Dates after the
        current date are not valid.
    fx_pricing_preferences : ~analyticsapi.models.FxPricingPreferences
        An object describing the fx calculation parameters.
    """

    valuation_date: Optional[datetime.date] = rest_field(name="valuationDate")
    """The date at which the instrument is valued. The value is expressed in ISO 8601 format:
     YYYY-MM-DD (e.g., '2021-01-01'). Dates after the current date are not valid."""
    fx_pricing_preferences: Optional["_models.FxPricingPreferences"] = rest_field(name="fxPricingPreferences")
    """An object describing the fx calculation parameters."""

    @overload
    def __init__(
        self,
        *,
        valuation_date: Optional[datetime.date] = None,
        fx_pricing_preferences: Optional["_models.FxPricingPreferences"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class QuoteInput(_model_base.Model):
    """An object used to get the instrument quote.

    Attributes
    ----------
    definition : ~analyticsapi.models.QuoteInputDefinition
        An object that defines the attributes for getting the instrument quote.
        Required.
    """

    definition: "_models.QuoteInputDefinition" = rest_field()
    """An object that defines the attributes for getting the instrument quote. Required."""

    @overload
    def __init__(
        self,
        definition: "_models.QuoteInputDefinition",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["definition"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class QuoteInputDefinition(_model_base.Model):
    """An object that defines the attributes for getting the instrument quote.

    Attributes
    ----------
    instrument_code : str
        The code (RIC) of the instrument. Required.
    """

    instrument_code: str = rest_field(name="instrumentCode")
    """The code (RIC) of the instrument. Required."""

    @overload
    def __init__(
        self,
        instrument_code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["instrument_code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class QuoteOutput(_model_base.Model):
    """An object that contains the instrument quote and related attributes.

    Readonly variables are only populated by the server, and will be ignored when sending a request.

    Attributes
    ----------
    start_date : ~datetime.date
        The start date of the instrument. Depending on the tenor the start date
        is defined as follows:

        * for ON and SPOT it is typically equal to the valuation date,
        * for TN it is the valuation date + 1D,
        * for post-spot tenors (1D, 1M, 1Y, etc.) it is the valuation date + spot lag.
          The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., '2023-01-01').
    end_date : ~datetime.date
        The maturity or expiry date of the instrument. The value is expressed
        in ISO 8601 format: YYYY-MM-DD (e.g., '2024-01-01').
    definition : ~analyticsapi.models.QuoteOutputDefinition
        An object that defines the attributes for getting the instrument quote.
        Required.
    values_property : ~analyticsapi.models.BidAskValues
        An object that contains the bid and ask quotes for the instrument.
    """

    start_date: Optional[datetime.date] = rest_field(name="startDate", visibility=["read"])
    """The start date of the instrument. Depending on the tenor the start date is defined as follows:
     
     
     * for ON and SPOT it is typically equal to the valuation date,
     * for TN it is the valuation date + 1D,
     * for post-spot tenors (1D, 1M, 1Y, etc.) it is the valuation date + spot lag.
       The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., '2023-01-01')."""
    end_date: Optional[datetime.date] = rest_field(name="endDate", visibility=["read"])
    """The maturity or expiry date of the instrument. The value is expressed in ISO 8601 format:
     YYYY-MM-DD (e.g., '2024-01-01')."""
    definition: "_models.QuoteOutputDefinition" = rest_field()
    """An object that defines the attributes for getting the instrument quote. Required."""
    values_property: Optional["_models.BidAskValues"] = rest_field(name="values")
    """An object that contains the bid and ask quotes for the instrument."""

    @overload
    def __init__(
        self,
        *,
        definition: "_models.QuoteOutputDefinition",
        values_property: Optional["_models.BidAskValues"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class QuoteOutputDefinition(_model_base.Model):
    """An object that defines the attributes for getting the instrument quote.

    Attributes
    ----------
    instrument_code : str
        The code (RIC) of the instrument. Required.
    """

    instrument_code: str = rest_field(name="instrumentCode")
    """The code (RIC) of the instrument. Required."""

    @overload
    def __init__(
        self,
        instrument_code: str,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["instrument_code"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class RelativeAdjustableDate(Date, discriminator="RelativeAdjustableDate"):
    """RelativeAdjustableDate.

    Attributes
    ----------
    date_moving_convention : str or ~analyticsapi.models.DateMovingConvention
        The method to adjust dates to working days. The possible values are:
        ModifiedFollowing: dates are adjusted to the next business day
        convention unless it goes into the next month. In such case, the
        previous business day convention is used, NextBusinessDay: dates are
        moved to the following working day, PreviousBusinessDay: dates are
        moved to the preceding working day, NoMoving: dates are not adjusted,
        EveryThirdWednesday: dates are moved to the third Wednesday of the
        month, or to the next working day if the third Wednesday is not a
        working day, BbswModifiedFollowing: dates are adjusted to the next
        business day convention unless it goes into the next month, or crosses
        mid-month (15th). In such case, the previous business day convention is
        used. Default is ModifiedFollowing. Known values are:
        "ModifiedFollowing", "NextBusinessDay", "PreviousBusinessDay",
        "NoMoving", "EveryThirdWednesday", and "BbswModifiedFollowing".
    calendars : list[~analyticsapi.models.CalendarRelatedResource]
        An array of calendars that should be used for the date adjustment.
        Typically the calendars are derived based on the instruments currency
        or crossCurrency code.
    date_type : str or ~analyticsapi.models.RELATIVE_ADJUSTABLE_DATE
        The type of the Date input. Possible values are: AdjustableDate,
        RelativeAdjustableDate. Required.
    tenor : str
        A code indicating the length of the period between the start date and
        the end date of the instrument. Predefined values are: ON (Overnight -
        A one business day period that starts today), TN (Tomorrow-Next - A one
        business day period that starts next business day, SPOT (Spot Date), SN
        (Spot-Next - A one business day period that starts at the spot date of
        a currency pair) or SW (Spot-Week - A one business week period that
        starts at the spot date of a currency pair). Tenors can also be
        specified as a whole number of time units. Possible units are: D
        (Days), W (Weeks), M (Months) or Y (Years). For example, one month is
        written '1M', 3 years is written: '3Y'. Time units can be mixed.  For
        example, 5M3D means '5 months and 3 days'. Note: units must be written
        in descending order of size (Y > M > W > D). Required.
    reference_date : str or ~analyticsapi.models.ReferenceDate
        The date which has been used as a reference date for the provided
        tenor. Possible values are: StartDate, ValuationDate, SpotDate. Default
        is StartDate. Known values are: "SpotDate", "StartDate", and
        "ValuationDate".
    """

    date_type: Literal[DateType.RELATIVE_ADJUSTABLE_DATE] = rest_discriminator(name="dateType")  # type: ignore
    """The type of the Date input. Possible values are: AdjustableDate, RelativeAdjustableDate.
     Required."""
    tenor: str = rest_field()
    """A code indicating the length of the period between the start date and the end date of the
     instrument.
     Predefined values are: ON (Overnight - A one business day period that starts today), TN
     (Tomorrow-Next - A one business day period that starts next business day, SPOT (Spot Date), SN
     (Spot-Next - A one business day period that starts at the spot date of a currency pair) or SW
     (Spot-Week - A one business week period that starts at the spot date of a currency pair).
     Tenors can also be specified as a whole number of time units. Possible units are: D (Days), W
     (Weeks), M (Months) or Y (Years). For example, one month is written '1M', 3 years is written:
     '3Y'.
     Time units can be mixed.  For example, 5M3D means '5 months and 3 days'. Note: units must be
     written in descending order of size (Y > M > W > D). Required."""
    reference_date: Optional[Union[str, "_models.ReferenceDate"]] = rest_field(name="referenceDate")
    """The date which has been used as a reference date for the provided tenor. Possible values are:
     StartDate, ValuationDate, SpotDate. Default is StartDate. Known values are: \"SpotDate\",
     \"StartDate\", and \"ValuationDate\"."""

    @overload
    def __init__(
        self,
        *,
        tenor: str,
        date_moving_convention: Optional[Union[str, "_models.DateMovingConvention"]] = None,
        calendars: Optional[List["_models.CalendarRelatedResource"]] = None,
        reference_date: Optional[Union[str, "_models.ReferenceDate"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, date_type=DateType.RELATIVE_ADJUSTABLE_DATE, **kwargs)
        if self.calendars is None:
            self.calendars = list()


class RelativePositionWhen(When, discriminator="RelativePositionWhen"):
    """Relative position annual rule. For example, Summer holiday on last Monday of August.

    Attributes
    ----------
    position_type : str or ~analyticsapi.models.RELATIVE_POSITION_WHEN
        The type of regular annual holiday rule. Only RelativePositionWhen
        value applies. Required. The holiday falls on a day of the week in a
        certain month. For example, Summer holiday on last Monday of August.
    index : str or ~analyticsapi.models.IndexOrder
        The ordinal number of the day of the week in the month. Required. Known
        values are: "First", "Second", "Third", "Fourth", and "Last".
    dayof_week : str or ~analyticsapi.models.WeekDay
        The day of the week. Required. Known values are: "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Saturday", and "Sunday".
    month : str or ~analyticsapi.models.Month
        The month of the year. Required. Known values are: "January",
        "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", and "December".
    """

    position_type: Literal[PositionType.RELATIVE_POSITION_WHEN] = rest_discriminator(name="positionType")  # type: ignore
    """The type of regular annual holiday rule. Only RelativePositionWhen value applies. Required. The
     holiday falls on a day of the week in a certain month. For example, Summer holiday on last
     Monday of August."""
    index: Union[str, "_models.IndexOrder"] = rest_field()
    """The ordinal number of the day of the week in the month. Required. Known values are: \"First\",
     \"Second\", \"Third\", \"Fourth\", and \"Last\"."""
    dayof_week: Union[str, "_models.WeekDay"] = rest_field(name="dayofWeek")
    """The day of the week. Required. Known values are: \"Monday\", \"Tuesday\", \"Wednesday\",
     \"Thursday\", \"Friday\", \"Saturday\", and \"Sunday\"."""
    month: Union[str, "_models.Month"] = rest_field()
    """The month of the year. Required. Known values are: \"January\", \"February\", \"March\",
     \"April\", \"May\", \"June\", \"July\", \"August\", \"September\", \"October\", \"November\",
     and \"December\"."""

    @overload
    def __init__(
        self,
        *,
        index: Union[str, "_models.IndexOrder"],
        dayof_week: Union[str, "_models.WeekDay"],
        month: Union[str, "_models.Month"],
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, position_type=PositionType.RELATIVE_POSITION_WHEN, **kwargs)


class RelativeRescheduleDescription(RescheduleDescription, discriminator="RelativeRescheduleDescription"):
    """An object to determine the rule for rescheduling a holiday to a specific day.

    Attributes
    ----------
    reschedule_type : str or ~analyticsapi.models.RELATIVE_RESCHEDULE_DESCRIPTION
        The type of rescheduling for the observation period. Only
        RelativeRescheduleRescheduleDescription value applies. Required.
        Reschedule the holiday to a specific day. For example, if a holiday
        falls on Sunday, it is rescheduled to the first Monday after the
        holiday.
    index : str or ~analyticsapi.models.IndexOrder
        The ordinal number of the day of the week in the month. The 'Last'
        value should only be used if the direction is set to 'Before'.
        Required. Known values are: "First", "Second", "Third", "Fourth", and
        "Last".
    dayof_week : str or ~analyticsapi.models.WeekDay
        The day of the week. Required. Known values are: "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Saturday", and "Sunday".
    direction : str or ~analyticsapi.models.Direction
        An indicator of whether the observation period falls before or after
        the reference point. Required. Known values are: "Before" and "After".
    """

    reschedule_type: Literal[RescheduleType.RELATIVE_RESCHEDULE_DESCRIPTION] = rest_discriminator(name="rescheduleType")  # type: ignore
    """The type of rescheduling for the observation period. Only
     RelativeRescheduleRescheduleDescription value applies. Required. Reschedule the holiday to a
     specific day. For example, if a holiday falls on Sunday, it is rescheduled to the first Monday
     after the holiday."""
    index: Union[str, "_models.IndexOrder"] = rest_field()
    """The ordinal number of the day of the week in the month. The 'Last' value should only be used if
     the direction is set to 'Before'. Required. Known values are: \"First\", \"Second\", \"Third\",
     \"Fourth\", and \"Last\"."""
    dayof_week: Union[str, "_models.WeekDay"] = rest_field(name="dayofWeek")
    """The day of the week. Required. Known values are: \"Monday\", \"Tuesday\", \"Wednesday\",
     \"Thursday\", \"Friday\", \"Saturday\", and \"Sunday\"."""
    direction: Union[str, "_models.Direction"] = rest_field()
    """An indicator of whether the observation period falls before or after the reference point.
     Required. Known values are: \"Before\" and \"After\"."""

    @overload
    def __init__(
        self,
        *,
        index: Union[str, "_models.IndexOrder"],
        dayof_week: Union[str, "_models.WeekDay"],
        direction: Union[str, "_models.Direction"],
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, reschedule_type=RescheduleType.RELATIVE_RESCHEDULE_DESCRIPTION, **kwargs)


class RelativeToRulePositionWhen(When, discriminator="RelativeToRulePositionWhen"):
    """RelativeToRulePosition position annual holiday rule. This defines the holiday period by
    reference to another holiday rule. Easter is most commonly used as a reference point.

    Attributes
    ----------
    position_type : str or ~analyticsapi.models.RELATIVE_TO_RULE_POSITION_WHEN
        The type of regular annual holiday rule. Only
        RelativeToRulePositionWhen value applies. Required. The timing of the
        holiday depends on the timing of another holiday. For example, Easter
        is most commonly used as a reference point.
    key : str
        A user-defined key to create a reference to another rule (e.g. Easter).
        Required.
    reschedule_description : ~analyticsapi.models.RescheduleDescription
        An object to determine holiday rescheduling. Required.
    """

    position_type: Literal[PositionType.RELATIVE_TO_RULE_POSITION_WHEN] = rest_discriminator(name="positionType")  # type: ignore
    """The type of regular annual holiday rule. Only RelativeToRulePositionWhen value applies.
     Required. The timing of the holiday depends on the timing of another holiday. For example,
     Easter is most commonly used as a reference point."""
    key: str = rest_field()
    """A user-defined key to create a reference to another rule (e.g. Easter). Required."""
    reschedule_description: "_models.RescheduleDescription" = rest_field(name="rescheduleDescription")
    """An object to determine holiday rescheduling. Required."""

    @overload
    def __init__(
        self,
        *,
        key: str,
        reschedule_description: "_models.RescheduleDescription",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, position_type=PositionType.RELATIVE_TO_RULE_POSITION_WHEN, **kwargs)


class RestDays(_model_base.Model):
    """An object to determine rest days for the calendar.

    Attributes
    ----------
    rest_days : list[str or ~analyticsapi.models.WeekDay]
        Days of the week that are set as rest days. An array of WeekDay
        objects. Default is [WeekDay.Saturday, WeekDay.Sunday]. Required.
    validity_period : ~analyticsapi.models.ValidityPeriod
        An object to determine the validity period. If not specified, the
        validity period is assumed to be perpetual.
    """

    rest_days: List[Union[str, "_models.WeekDay"]] = rest_field(name="restDays")
    """Days of the week that are set as rest days. An array of WeekDay objects. Default is
     [WeekDay.Saturday, WeekDay.Sunday]. Required."""
    validity_period: Optional["_models.ValidityPeriod"] = rest_field(name="validityPeriod")
    """An object to determine the validity period. If not specified, the validity period is assumed to
     be perpetual."""

    @overload
    def __init__(
        self,
        *,
        rest_days: List[Union[str, "_models.WeekDay"]],
        validity_period: Optional["_models.ValidityPeriod"] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.rest_days is None:
            self.rest_days = list()


class ServiceError(_model_base.Model):
    """An object that contains the information in case of a blocking error in a calculation.

    Attributes
    ----------
    id : str
        The identifier of the error. Required.
    code : str
        The code of the error. Required.
    message : str
        The message in case of a blocking error in the calculation. Required.
    status : str
        The status of the error.
    errors : list[~analyticsapi.models.InnerError]
        An array of objects that contains the detailed information in case of a
        blocking error in the calculation.
    """

    id: str = rest_field()
    """The identifier of the error. Required."""
    code: str = rest_field()
    """The code of the error. Required."""
    message: str = rest_field()
    """The message in case of a blocking error in the calculation. Required."""
    status: Optional[str] = rest_field()
    """The status of the error."""
    errors: Optional[List["_models.InnerError"]] = rest_field()
    """An array of objects that contains the detailed information in case of a blocking error in the
     calculation."""

    @overload
    def __init__(
        self,
        *,
        id: str,  # pylint: disable=redefined-builtin
        code: str,
        message: str,
        status: Optional[str] = None,
        errors: Optional[List["_models.InnerError"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.errors is None:
            self.errors = list()


class ServiceErrorResponse(_model_base.Model):
    """The information returned in an error response.

    Attributes
    ----------
    error : ~analyticsapi.models.ServiceError
        An object that contains the information in case of a blocking error in
        a calculation. Required.
    """

    error: "_models.ServiceError" = rest_field()
    """An object that contains the information in case of a blocking error in a calculation. Required."""

    @overload
    def __init__(
        self,
        error: "_models.ServiceError",
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        if len(args) == 1 and not isinstance(args[0], dict):
            kwargs["error"] = args[0]
            args = tuple()
        super().__init__(*args, **kwargs)


class Time(_model_base.Model):
    """Time and timezone specification.

    Attributes
    ----------
    local_time : ~datetime.time
        The specified time expressed in hh:mm:ss format (e.g., '17:00:00').
        Required.
    time_zone_id : str
        The time zone of the specified time.
    """

    local_time: datetime.time = rest_field(name="localTime")
    """The specified time expressed in hh:mm:ss format (e.g., '17:00:00'). Required."""
    time_zone_id: Optional[str] = rest_field(name="timeZoneId")
    """The time zone of the specified time."""

    @overload
    def __init__(
        self,
        *,
        local_time: datetime.time,
        time_zone_id: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)


class UnderlyingCurves(_model_base.Model):
    """An object that contains the underlying curves used to construct the curve.

    Attributes
    ----------
    fx_forward_curves : list[~analyticsapi.models.FxUnderlyingCurve]
        An array of objects that contains the underlying cross currency curves
        used to construct the curve.
    interest_rate_curves : list[~analyticsapi.models.IrUnderlyingCurve]
        An array of objects that contains the underlying interest rate curves
        used to construct the curve.
    """

    fx_forward_curves: Optional[List["_models.FxUnderlyingCurve"]] = rest_field(name="fxForwardCurves")
    """An array of objects that contains the underlying cross currency curves used to construct the
     curve."""
    interest_rate_curves: Optional[List["_models.IrUnderlyingCurve"]] = rest_field(name="interestRateCurves")
    """An array of objects that contains the underlying interest rate curves used to construct the
     curve."""

    @overload
    def __init__(
        self,
        *,
        fx_forward_curves: Optional[List["_models.FxUnderlyingCurve"]] = None,
        interest_rate_curves: Optional[List["_models.IrUnderlyingCurve"]] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.fx_forward_curves is None:
            self.fx_forward_curves = list()
        if self.interest_rate_curves is None:
            self.interest_rate_curves = list()


class ValidityPeriod(_model_base.Model):
    """An object to determine the validity period.

    Attributes
    ----------
    start_date : ~datetime.date
        The start date of the validity period. The value is expressed in ISO
        8601 format: YYYY-MM-DD (e.g., 2023-01-01).
    end_date : ~datetime.date
        The end date of the validity period. The value is expressed in ISO 8601
        format: YYYY-MM-DD (e.g., 2024-01-01).
    """

    start_date: Optional[datetime.date] = rest_field(name="startDate")
    """The start date of the validity period. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., 2023-01-01)."""
    end_date: Optional[datetime.date] = rest_field(name="endDate")
    """The end date of the validity period. The value is expressed in ISO 8601 format: YYYY-MM-DD
     (e.g., 2024-01-01)."""

    @overload
    def __init__(
        self,
        *,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        Parameters
        ----------
        mapping : Mapping[str, Any]
            raw JSON to initialize the model.
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)
