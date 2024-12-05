# coding=utf-8


from enum import Enum

from corehttp.utils import CaseInsensitiveEnumMeta


class DateMovingConvention(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The method to adjust dates to working days."""

    MODIFIED_FOLLOWING = "ModifiedFollowing"
    """Dates are moved to the next working day unless it falls on the next month. In such case,
    PreviousBusinessDay convention is used.
    """
    NEXT_BUSINESS_DAY = "NextBusinessDay"
    """Dates are moved to the next working day."""
    PREVIOUS_BUSINESS_DAY = "PreviousBusinessDay"
    """Dates are moved to the previous working day."""
    NO_MOVING = "NoMoving"
    """Dates are not adjusted."""
    EVERY_THIRD_WEDNESDAY = "EveryThirdWednesday"
    """Dates are moved to the third Wednesday of the month, or to the next working day if the third
    Wednesday is not a working day.
    """
    BBSW_MODIFIED_FOLLOWING = "BbswModifiedFollowing"
    """Dates are moved to the next working day unless it falls on the next month, or crosses mid-month
    (15th). In such case, PreviousBusinessDay convention is used.
    """


class DateType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of DateType."""

    ADJUSTABLE_DATE = "AdjustableDate"
    RELATIVE_ADJUSTABLE_DATE = "RelativeAdjustableDate"


class DayCountBasis(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The day count basis convention used to calculate the period between two dates."""

    DCB_30_360 = "Dcb_30_360"
    """For two dates (Y1,M1,D1) and (Y2,M2,D2) the number of days in the period is defined as:
    (D2−D1)+(M2−M1)×30+(Y2−Y1)×360. The year basis is 360 days.

    Date adjustment rules (to be applied in order):

    #. If D1 is the last day of the month, change D1 to 30.
    #. If D1=30, then D2=min(D2,30).
    """
    DCB_30_360_US = "Dcb_30_360_US"
    """For two dates (Y1,M1,D1) and (Y2,M2,D2) the number of days in the period is defined as:
    (D2−D1)+(M2−M1)×30+(Y2−Y1)×360. The year basis is 360 days.

    Date adjustment rules (to be applied in order):

    #. If D1 is the last day of the month, change D1 to 30.
    #. If D1=30 then, D2=min(D2,30).
    #. If D1 and D2 are the last day of February, then D2=30.
    """
    DCB_30_360_GERMAN = "Dcb_30_360_German"
    """For two dates (Y1,M1,D1) and (Y2,M2,D2) the number of days in the period is defined as:
    (D2−D1)+(M2−M1)×30+(Y2−Y1)×360. The year basis is 360 days.

    Date adjustment rules (to be applied in order):

    #. If D1 or D2 is 31, change it to 30.
    #. If D1 or D2 is February 29th, change it to 30.
    """
    DCB_30_360_ISDA = "Dcb_30_360_ISDA"
    """For two dates (Y1,M1,D1) and (Y2,M2,D2) the number of days in the period is defined as:
    (D2−D1)+(M2−M1)×30+(Y2−Y1)×360. The year basis is 360 days.

    Date adjustment rules (to be applied in order):

    #. D1=min(D1,30).
    #. If D1=30, then D2=min(D2,30).
    """
    DCB_30_365_ISDA = "Dcb_30_365_ISDA"
    """Similar to Dcb_30_360_ISDA convention, except that the year basis is 365 days."""
    DCB_30_365_GERMAN = "Dcb_30_365_German"
    """Similar to Dcb_30_360_German convention, except that the year basis is 365 days."""
    DCB_30_365_BRAZIL = "Dcb_30_365_Brazil"
    """Similar to Dcb_30_360_US convention, except that the year basis is 365 days."""
    DCB_30_ACTUAL_GERMAN = "Dcb_30_Actual_German"
    """Similar to Dcb_30_360_German convention, except that the year basis is the actual number of
    days in the year.
    """
    DCB_30_ACTUAL = "Dcb_30_Actual"
    """Similar to Dcb_30_360_US convention, except that the year basis is the actual number of days in
    the year.
    """
    DCB_30_ACTUAL_ISDA = "Dcb_30_Actual_ISDA"
    """Similar to Dcb_30_360_ISDA convention, except that the year basis is the actual number of days
    in the year.
    """
    DCB_30_E_360_ISMA = "Dcb_30E_360_ISMA"
    """The actual number of days in the coupon period is used.
    But it is calculated on the year basis of 360 days with twelve 30-day months (regardless of the
    date of the first day or last day of the period).
    """
    DCB_ACTUAL_360 = "Dcb_Actual_360"
    """The actual number of days in the period is used. The year basis is 360 days."""
    DCB_ACTUAL_364 = "Dcb_Actual_364"
    """The actual number of days in the period is used. The year basis is 364 days."""
    DCB_ACTUAL_365 = "Dcb_Actual_365"
    """The actual number of days in the period is used. The year basis is 365 days."""
    DCB_ACTUAL_ACTUAL = "Dcb_Actual_Actual"
    """The actual number of days in the period is used. The year basis is the actual number of days in
    the year.
    """
    DCB_ACTUAL_ACTUAL_ISDA = "Dcb_Actual_Actual_ISDA"
    """Similar to Dcb_Actual_365 convention, except that on a leap year the year basis is 366 days.
    The period is calculated as: the number of days in a leap year/366 + the number of days in a
    non-leap year/365.
    """
    DCB_ACTUAL_ACTUAL_AFB = "Dcb_Actual_Actual_AFB"
    """The actual number of days in the period is used. The year basis is 366 days if the calculation
    period contains February 29th, otherwise it is 365 days.
    """
    DCB_WORKING_DAYS_252 = "Dcb_WorkingDays_252"
    """The actual number of business days in the period according to a given calendar is used. The
    year basis is 252 days.
    """
    DCB_ACTUAL_365_L = "Dcb_Actual_365L"
    """The actual number of days in the period is used. The year basis is calculated as follows:
    If the coupon frequency is annual and February 29th is included in the period, the year basis
    is 366 days, otherwise it is 365 days.
    If the coupon frequency is not annual, the year basis is 366 days for each coupon period whose
    end date falls in a leap year, otherwise it is 365.
    """
    DCB_ACTUAL_365_P = "Dcb_Actual_365P"
    DCB_ACTUAL_LEAP_DAY_365 = "Dcb_ActualLeapDay_365"
    """The actual number of days in the period is used, but February 29th is ignored for a leap year
    when counting days. The year basis is 365 days."""
    DCB_ACTUAL_LEAP_DAY_360 = "Dcb_ActualLeapDay_360"
    """The actual number of days in the period is used, but February 29th is ignored for a leap year
    when counting days. The year basis is 360 days.
    """
    DCB_ACTUAL_36525 = "Dcb_Actual_36525"
    """The actual number of days in the period is used. The year basis is 365.25 days."""
    DCB_ACTUAL_365_CANADIAN_CONVENTION = "Dcb_Actual_365_CanadianConvention"
    """The actual number of days in the period is used. If it is less than one regular coupon period,
    the year basis is 365 days.
    Otherwise, the day count is defined as: 1 – days remaining in the period x Frequency / 365.
    In most cases, Canadian domestic bonds have semiannual coupons.
    """
    DCB_CONSTANT = "Dcb_Constant"


class Direction(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """An indicator of whether the observation period falls before or after the reference point."""

    BEFORE = "Before"
    AFTER = "After"


class DurationType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of the holiday - Possible values are FullDayDuration (full days) or HalfDayDuration
    (half days).
    """

    FULL_DAY_DURATION = "FullDayDuration"
    """Full days where the no trading takes place."""
    HALF_DAY_DURATION = "HalfDayDuration"
    """Half day holidays. Designed to account for the days the markets are open, but not for a full
    trading session.
    """


class ExtrapolationMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The extrapolation method used in the curve bootstrapping."""

    NONE = "None"
    """No extrapolation."""
    CONSTANT = "Constant"
    """Constant extrapolation."""
    LINEAR = "Linear"
    """Linear extrapolation."""


class Frequency(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of Frequency."""

    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "BiWeekly"
    MONTHLY = "Monthly"


class FxForwardCurveConstituentType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """FX Forward curve constituent type. Possible values are: "FxSpot", "FxForward",
    "CrossCurrencySwap", and "Deposit".
    """

    FX_SPOT = "FxSpot"
    FX_FORWARD = "FxForward"
    CROSS_CURRENCY_SWAP = "CrossCurrencySwap"
    DEPOSIT = "Deposit"


class FxForwardCurveInterpolationMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The interpolation method used in the curve bootstrapping."""

    CUBIC_SPLINE = "CubicSpline"
    """Local cubic interpolation of discount factors."""
    CONSTANT = "Constant"
    """Constant interpolation."""
    LINEAR = "Linear"
    """Linear interpolation."""
    CUBIC_DISCOUNT = "CubicDiscount"


class IndexOrder(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The ordinal number of the day of the week in the month when defining holiday timing. For
    example, a rule for the last Monday of September would use "Last" in its definition.
    """

    FIRST = "First"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    LAST = "Last"


class Month(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Months of the year. Month names written in full."""

    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


class PeriodType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The method of the period calculation."""

    WORKING_DAY = "WorkingDay"
    """Only working days are taken into account."""
    NON_WORKING_DAY = "NonWorkingDay"
    """Only non-working days are taken into account."""
    DAY = "Day"
    """All calendar days are taken into account."""
    WEEK = "Week"
    """The period is calculated in weeks."""
    MONTH = "Month"
    """The period is calculated in months."""
    QUARTER = "Quarter"
    """The period is calculated in quarters."""
    YEAR = "Year"
    """The period is calculated in years."""


class PeriodTypeOutput(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of the calculated period. Possible values are: Day, WorkingDay, Week, Month, Quarter
    or Year.
    """

    DAY = "Day"
    WORKING_DAY = "WorkingDay"
    WEEK = "Week"
    MONTH = "Month"
    QUARTER = "Quarter"
    YEAR = "Year"


class PositionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of regular annual holiday rule. Possible values are: AbsolutePositionWhen (for fixed
    dates), RelativePositionWhen (for a holiday that falls on a particular weekday in a month), or
    RelativeToRulePositionWhen (for a holiday that depends on the timing of another holiday).
    """

    ABSOLUTE_POSITION_WHEN = "AbsolutePositionWhen"
    """The holiday is on a fixed date. For example, New Year holiday on January 1."""
    RELATIVE_POSITION_WHEN = "RelativePositionWhen"
    """The holiday falls on a day of the week in a certain month. For example, Summer holiday on last
    Monday of August.
    """
    RELATIVE_TO_RULE_POSITION_WHEN = "RelativeToRulePositionWhen"
    """The timing of the holiday depends on the timing of another holiday. For example, Easter is most
    commonly used as a reference point.
    """


class ReferenceDate(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of ReferenceDate."""

    SPOT_DATE = "SpotDate"
    START_DATE = "StartDate"
    VALUATION_DATE = "ValuationDate"


class RescheduleType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of rescheduling for the holiday observation period."""

    LAG_DAYS_RESCHEDULE_DESCRIPTION = "LagDaysRescheduleDescription"
    """Reschedule the holiday by specifying a lag period in days. For example, if a holiday falls on
    Sunday, it can be moved by one day so that it happens on the following Monday.
    """
    RELATIVE_RESCHEDULE_DESCRIPTION = "RelativeRescheduleDescription"
    """Reschedule the holiday to a specific day. For example, if a holiday falls on Sunday, it is
    rescheduled to the first Monday after the holiday.
    """


class ResourceType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve, FxForwardCurve,
    Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    """

    CALENDAR = "Calendar"
    CURRENCY = "Currency"
    CROSS_CURRENCY = "CrossCurrency"
    IR_CURVE = "IrCurve"
    FX_FORWARD_CURVE = "FxForwardCurve"
    ANALYTICS = "Analytics"
    LOAN = "Loan"
    FX_SPOT = "FxSpot"
    FX_FORWARD = "FxForward"
    NON_DELIVERABLE_FORWARD = "NonDeliverableForward"
    DEPOSIT = "Deposit"
    CROSS_CURRENCY_SWAP = "CrossCurrencySwap"
    SPACE = "Space"
    INSTRUMENT = "Instrument"


class SettlementType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of SettlementType."""

    CASH = "Cash"
    PHYSICAL = "Physical"


class Status(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Status of the resource."""

    ACTIVE = "Active"
    DELETED = "Deleted"


class TenorType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The tenor type."""

    ODD = "Odd"
    LONG = "Long"
    """Long-term tenor."""
    IMM = "IMM"
    """Tenor, end date of which is the third Wednesday of March, June, September and December."""
    BEGINNING_OF_MONTH = "BeginningOfMonth"
    """Tenor, end date of which is the first business day of the month."""
    END_OF_MONTH = "EndOfMonth"
    """Tenor, end date of which is the last business day of the month."""


class WeekDay(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Days of the week. Day names written in full."""

    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class YearBasis(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Year basis convention for a currency. Possible values are 360 or 365."""

    ENUM_360 = "360"
    ENUM_365 = "365"
