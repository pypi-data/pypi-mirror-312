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
    CalendarRelatedResource,
    CurrencyAsCollectionItem,
    CurrencyDefinition,
    Description,
    Location,
    YearBasis,
)

from ._currency import Currency
from ._logger import logger

__all__ = [
    "CalendarRelatedResource",
    "CurrencyAsCollectionItem",
    "CurrencyDefinition",
    "delete",
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
    Load a Currency using its name and space

    Parameters
    ----------
    resource_id : str, optional
        The Currency id.
        Required if name is not provided.
    name : str, optional
        The Currency name.
        Required if resource_id is not provided. The name parameter must be specified when the object is first created. Thereafter it is optional.
    space : str, optional
        The space where the Currency is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    Currency
        The Currency instance.

    Examples
    --------


    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            logger.warn("resource_id argument received, name & space arguments are ignored")
        return _load_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Load Currency {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"Currency {name} not found in space={space!r}")
        raise ResourceNotFound(f"Resource Currency not found by identifier name={name} space={space}")
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
    Delete Currency instance from the server.

    Parameters
    ----------
    resource_id : str, optional
        The Currency resource ID.
        Required if name is not provided.
    name : str, optional
        The Currency name.
        Required if resource_id is not provided.
    space : str, optional
        The space where the Currency is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    ServiceErrorResponse, optional
        Error response, if applicable, otherwise None

    Examples
    --------


    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            logger.warn("resource_id argument received, name & space arguments are ignored")
        return _delete_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Delete Currency {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"Currency {name} not found in space={space!r}")
        raise ResourceNotFound(f"Resource Currency not found by identifier name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    return _delete_by_id(result[0].id)


def _delete_by_id(currency_id: str) -> bool:
    """
    Delete resource.

    Parameters
    ----------
    currency_id : str
        A sequence of textual characters.

    Returns
    --------
    bool


    Examples
    --------


    """

    try:
        logger.info(f"Deleting CurrencyResource with id:  {currency_id}")
        check_and_raise(Client().currency_resource.delete(currency_id=currency_id))
        logger.info(f"Deleted CurrencyResource with id:  {currency_id}")

        return True
    except Exception as err:
        logger.error(f"Error deleting CurrencyResource with id:  {currency_id}")
        check_exception_and_raise(err)


def _load_by_id(currency_id: str) -> Currency:
    """
    Read resource

    Parameters
    ----------
    currency_id : str
        A sequence of textual characters.

    Returns
    --------
    Currency


    Examples
    --------


    """

    try:
        logger.info(f"Opening CurrencyResource with id:  {currency_id}")

        response = check_and_raise(Client().currency_resource.read(currency_id=currency_id))

        output = Currency(response.data.definition, response.data.description)

        output._id = response.data.id

        output._location = response.data.location

        return output
    except Exception as err:
        logger.error(f"Error opening CurrencyResource:  {err}")
        check_exception_and_raise(err)


def search(
    *,
    item_per_page: Optional[int] = None,
    names: Optional[List[str]] = None,
    spaces: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> List[CurrencyAsCollectionItem]:
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
    List[CurrencyAsCollectionItem]
        An object describing the basic properties of a currency.

    Examples
    --------


    """

    try:
        logger.info(f"Calling search")

        response = check_and_raise(
            Client().currencies_resource.list(item_per_page=item_per_page, names=names, spaces=spaces, tags=tags)
        )

        output = response.data
        logger.info(f"Called search")

        return output
    except Exception as err:
        logger.error(f"Error search {err}")
        check_exception_and_raise(err)
