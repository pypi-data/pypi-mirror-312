import copy
import datetime
from typing import Any, Dict, List, Optional, Union

from lseg_analytics._client.client import Client
from lseg_analytics.common._resource_base import ResourceBase
from lseg_analytics.exceptions import (
    LibraryException,
    ResourceNotFound,
    check_and_raise,
    check_exception_and_raise,
)
from lseg_analytics_basic_client.models import (
    CrossCurrencyAsCollectionItem,
    CrossCurrencyDefinition,
    Description,
    Location,
    ResourceType,
)

from ._logger import logger


class CrossCurrency(ResourceBase):
    """
    CrossCurrency object.

    Contains all the necessary information to identify and define a CrossCurrency instance.

    Attributes
    ----------
    type : Union[str, ResourceType], optional
        The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str, optional
        Unique resource ID specified by LSEG.
    location : Location
        Location of the platform where resource is stored.
    description : Description, optional
        Description object that contains the resource summary and tags.
    definition : CrossCurrencyDefinition
        The definition of the cross currency.

    See Also
    --------


    Examples
    --------


    """

    _definition_class = CrossCurrencyDefinition

    def __init__(
        self,
        definition: CrossCurrencyDefinition,
        description: Optional[Description] = None,
    ):
        """
        CrossCurrency constructor

        Parameters
        ----------
        definition : CrossCurrencyDefinition
            The definition of the cross currency.
        description : Description, optional
            Description object that contains the resource summary and tags.

        Examples
        --------


        """
        self.definition: CrossCurrencyDefinition = definition
        self.type: Optional[Union[str, ResourceType]] = "CrossCurrency"
        if description is None:
            self.description: Optional[Description] = Description(tags=[])
        else:
            self.description: Optional[Description] = description
        self._location: Location = Location(name="")
        self._id: Optional[str] = None

    @property
    def id(self):
        """
        Returns the CrossCurrency id

        Parameters
        ----------


        Returns
        --------
        str
            Unique resource ID specified by LSEG.

        Examples
        --------


        """
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("id is read only")

    @property
    def location(self):
        """
        Returns the CrossCurrency location

        Parameters
        ----------


        Returns
        --------
        Location
            Location of the platform where resource is stored.

        Examples
        --------


        """
        return self._location

    @location.setter
    def location(self, value):
        raise AttributeError("location is read only")

    def _create(self, location: Location) -> None:
        """
        Create resource.

        Parameters
        ----------
        location : Location
            Location of the platform where resource is stored.

        Returns
        --------
        None


        Examples
        --------


        """

        try:
            logger.info(f"Creating CrossCurrencyResource")

            response = check_and_raise(
                Client().cross_currencies_resource.create(
                    location=location,
                    description=self.description,
                    definition=self.definition,
                )
            )

            self._id = response.data.id

            self._location = response.data.location
            logger.info(f"CrossCurrencyResource created with id:  {self._id}")
        except Exception as err:
            logger.error(f"Error creating CrossCurrencyResource:  {err}")
            raise err

    def _overwrite(self) -> None:
        """
        Overwrite resource

        Parameters
        ----------


        Returns
        --------
        None


        Examples
        --------


        """
        logger.info(f"Overwriting CrossCurrencyResource with id: {self._id}")
        check_and_raise(
            Client().cross_currency_resource.overwrite(
                cross_currency_id=self._id,
                location=self._location,
                description=self.description,
                definition=self.definition,
            )
        )

    def save(self, *, name: Optional[str] = None, space: Optional[str] = None) -> bool:
        """
        Save CrossCurrency instance in the platform store.

        Parameters
        ----------
        name : str, optional
            The CrossCurrency name. The name parameter must be specified when the object is first created. Thereafter it is optional.
        space : str, optional
            The space where the CrossCurrency is stored.  Space is like a namespace where resources are stored.  By default there are two spaces:
            LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

        Returns
        --------
        bool, optional
            True, if saved successfully, otherwise None


        Examples
        --------


        """
        try:
            logger.info(f"Saving CrossCurrency")
            if self._id:
                if name and name != self._location.name or (space and space != self._location.space):
                    raise LibraryException("When saving an existing resource, you may not change the name or space")
                self._overwrite()
                logger.info(f"CrossCurrency saved")
            elif name:
                location = Location(name=name, space=space)
                self._create(location=location)
                logger.info(f"CrossCurrency saved to space: {self._location.space} name: {self._location.name}")
            else:
                raise LibraryException("When saving for the first time, name must be defined.")
            return True
        except Exception as err:
            logger.info(f"CrossCurrency save failed")
            check_exception_and_raise(err)

    def clone(self) -> "CrossCurrency":
        """
        Return the same object, without id, name and space

        Parameters
        ----------


        Returns
        --------
        CrossCurrency
            The cloned CrossCurrency object


        Examples
        --------


        """
        definition = self._definition_class()
        definition._data = copy.deepcopy(self.definition._data)
        description = None
        if self.description:
            description = Description()
            description._data = copy.deepcopy(self.description._data)
        return self.__class__(definition=definition, description=description)
