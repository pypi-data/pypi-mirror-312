# coding=utf-8


from ._operations import (
    calendarResourceOperations,
    calendarsResourceOperations,
    crossCurrenciesResourceOperations,
    crossCurrencyResourceOperations,
    currenciesResourceOperations,
    currencyResourceOperations,
    fxForwardCurveResourceOperations,
    fxForwardCurvesResourceOperations,
    fxForwardResourceOperations,
    fxForwardsResourceOperations,
    fxSpotResourceOperations,
    fxSpotsResourceOperations,
)
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import __all__ as _patch_all
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "calendarsResourceOperations",
    "calendarResourceOperations",
    "crossCurrenciesResourceOperations",
    "crossCurrencyResourceOperations",
    "currenciesResourceOperations",
    "currencyResourceOperations",
    "fxForwardCurvesResourceOperations",
    "fxForwardCurveResourceOperations",
    "fxForwardsResourceOperations",
    "fxForwardResourceOperations",
    "fxSpotsResourceOperations",
    "fxSpotResourceOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
