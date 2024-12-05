# coding=utf-8


from copy import deepcopy
from typing import Any, Awaitable

from corehttp.rest import AsyncHttpResponse, HttpRequest
from corehttp.runtime import AsyncPipelineClient, policies
from typing_extensions import Self

from .._serialization import Deserializer, Serializer
from ._configuration import AnalyticsAPIClientConfiguration
from .operations import (
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


class AnalyticsAPIClient:  # pylint: disable=client-accepts-api-version-keyword,too-many-instance-attributes
    """Analytic API to support channels workflows.

    :ivar calendars_resource: calendarsResourceOperations operations
    :vartype calendars_resource: analyticsapi.aio.operations.calendarsResourceOperations
    :ivar calendar_resource: calendarResourceOperations operations
    :vartype calendar_resource: analyticsapi.aio.operations.calendarResourceOperations
    :ivar cross_currencies_resource: crossCurrenciesResourceOperations operations
    :vartype cross_currencies_resource:
     analyticsapi.aio.operations.crossCurrenciesResourceOperations
    :ivar cross_currency_resource: crossCurrencyResourceOperations operations
    :vartype cross_currency_resource: analyticsapi.aio.operations.crossCurrencyResourceOperations
    :ivar currencies_resource: currenciesResourceOperations operations
    :vartype currencies_resource: analyticsapi.aio.operations.currenciesResourceOperations
    :ivar currency_resource: currencyResourceOperations operations
    :vartype currency_resource: analyticsapi.aio.operations.currencyResourceOperations
    :ivar fx_forward_curves_resource: fxForwardCurvesResourceOperations operations
    :vartype fx_forward_curves_resource:
     analyticsapi.aio.operations.fxForwardCurvesResourceOperations
    :ivar fx_forward_curve_resource: fxForwardCurveResourceOperations operations
    :vartype fx_forward_curve_resource:
     analyticsapi.aio.operations.fxForwardCurveResourceOperations
    :ivar fx_forwards_resource: fxForwardsResourceOperations operations
    :vartype fx_forwards_resource: analyticsapi.aio.operations.fxForwardsResourceOperations
    :ivar fx_forward_resource: fxForwardResourceOperations operations
    :vartype fx_forward_resource: analyticsapi.aio.operations.fxForwardResourceOperations
    :ivar fx_spots_resource: fxSpotsResourceOperations operations
    :vartype fx_spots_resource: analyticsapi.aio.operations.fxSpotsResourceOperations
    :ivar fx_spot_resource: fxSpotResourceOperations operations
    :vartype fx_spot_resource: analyticsapi.aio.operations.fxSpotResourceOperations
    :param endpoint: Service host. Default value is "https://api.analytics.lseg.com".
    :type endpoint: str
    """

    def __init__(  # pylint: disable=missing-client-constructor-parameter-credential
        self, endpoint: str = "https://api.analytics.lseg.com", **kwargs: Any
    ) -> None:
        _endpoint = "{endpoint}"
        self._config = AnalyticsAPIClientConfiguration(endpoint=endpoint, **kwargs)
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.logging_policy,
            ]
        self._client: AsyncPipelineClient = AsyncPipelineClient(endpoint=_endpoint, policies=_policies, **kwargs)

        self._serialize = Serializer()
        self._deserialize = Deserializer()
        self._serialize.client_side_validation = False
        self.calendars_resource = calendarsResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.calendar_resource = calendarResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.cross_currencies_resource = crossCurrenciesResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.cross_currency_resource = crossCurrencyResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.currencies_resource = currenciesResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.currency_resource = currencyResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_forward_curves_resource = fxForwardCurvesResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_forward_curve_resource = fxForwardCurveResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_forwards_resource = fxForwardsResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_forward_resource = fxForwardResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_spots_resource = fxSpotsResourceOperations(
            self._client, self._config, self._serialize, self._deserialize
        )
        self.fx_spot_resource = fxSpotResourceOperations(self._client, self._config, self._serialize, self._deserialize)

    def send_request(
        self, request: HttpRequest, *, stream: bool = False, **kwargs: Any
    ) -> Awaitable[AsyncHttpResponse]:
        """Runs the network request through the client's chained policies.

        >>> from corehttp.rest import HttpRequest
        >>> request = HttpRequest("GET", "https://www.example.org/")
        <HttpRequest [GET], url: 'https://www.example.org/'>
        >>> response = await client.send_request(request)
        <AsyncHttpResponse: 200 OK>

        For more information on this code flow, see https://aka.ms/azsdk/dpcodegen/python/send_request

        :param request: The network request you want to make. Required.
        :type request: ~corehttp.rest.HttpRequest
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call. Does not do error handling on your response.
        :rtype: ~corehttp.rest.AsyncHttpResponse
        """

        request_copy = deepcopy(request)
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }

        request_copy.url = self._client.format_url(request_copy.url, **path_format_arguments)
        return self._client.send_request(request_copy, stream=stream, **kwargs)  # type: ignore

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_details: Any) -> None:
        await self._client.__aexit__(*exc_details)
