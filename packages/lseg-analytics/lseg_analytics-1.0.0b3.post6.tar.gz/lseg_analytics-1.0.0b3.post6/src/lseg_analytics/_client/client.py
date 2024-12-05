import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests
from corehttp.runtime.policies import (
    BearerTokenCredentialPolicy,
    NetworkTraceLoggingPolicy,
)

from lseg_analytics.auth.machine_token_credential import MachineTokenCredential
from lseg_analytics.exceptions import (
    _ERROR_MESSAGE,
    ProxyAuthFailureError,
    ProxyNotEnabledError,
    ProxyNotFoundError,
    ProxyStatusError,
)
from lseg_analytics_basic_client import AnalyticsAPIClient

from ._logger import logger
from .config import load_config

__all__ = [
    "Client",
]


def _get_proxy_port_from_file():
    port_file = f'{os.path.expanduser("~")}{os.path.sep}.lseg{os.path.sep}VSCode{os.path.sep}.portInUse'

    if os.path.isfile(port_file):
        logger.info(f"Reading from file:{port_file}")
        with open(port_file) as f:
            port = f.read()
            if port.strip().strip("\n").lower() == "disabled":
                raise ProxyNotEnabledError(_ERROR_MESSAGE.PROXY_DISABLED.value)
            return int(port)
    else:
        raise Exception(f"Port file({port_file}) is not found")


def get_proxy_status_response(port):
    url = f"http://localhost:{port}/status"
    try:
        response = requests.get(url, timeout=1)  # timeout is 1 second
        return port, response
    except Exception as err:
        logger.warning(f"Get exception:{err} when requesting url :{url}")
        return port, None


def _check_proxy_status(ports_list):
    with ThreadPoolExecutor(max_workers=10) as exe:
        responses = exe.map(get_proxy_status_response, ports_list)
        for port, response in responses:
            try:
                if response is not None:
                    if response.status_code == 200:
                        data = json.loads(response.text)
                        if "lsegProxyEnabled" in data:
                            if data["lsegProxyEnabled"]:
                                return f"http://localhost:{port}"
                            else:
                                raise ProxyNotEnabledError(_ERROR_MESSAGE.PROXY_DISABLED.value)
                        else:
                            logger.error(
                                f"Failed to get status from proxy. lsegProxyEnabled is not in payload, Port: {port} Detail:{data}"
                            )
                            raise ProxyStatusError(_ERROR_MESSAGE.INVALID_RESPONSE.value)
                    elif response.status_code == 401:
                        raise ProxyAuthFailureError(_ERROR_MESSAGE.PROXY_UNAUTHORIZED.value)
                    elif response.status_code == 403:
                        raise ProxyAuthFailureError(_ERROR_MESSAGE.PROXY_FORBIDDEN.value)
                    else:
                        logger.error(
                            f"Failed to get status from proxy. Incorrect status code {response.status_code} with port: {port}"
                        )
                        raise ProxyStatusError(_ERROR_MESSAGE.INVALID_RESPONSE.value)
            except (ProxyStatusError, ProxyNotEnabledError, ProxyAuthFailureError) as err:
                raise err
            except Exception as err:
                logger.error(
                    f"Failed to get status from proxy. Got exception when parsing response with port {port}: {err}"
                )
                raise ProxyStatusError(_ERROR_MESSAGE.INVALID_RESPONSE.value)
    raise ProxyNotFoundError(_ERROR_MESSAGE.NO_AVALIABLE_PORT.value)


def _get_proxy_info():
    try:
        # add the port from file at first, so we will check it firstly
        port = _get_proxy_port_from_file()
        proxy_url = _check_proxy_status([port])
        logger.info(f"Proxy is found with port configured, proxy url is:{proxy_url}")
        return proxy_url
    except (ProxyStatusError, ProxyNotEnabledError, ProxyAuthFailureError) as err:
        raise err
    except Exception as err:  # No break
        logger.warning(f"Failed to load proxy port from local file, error: {err}")

    # add default ports: 60100 to 60110 inclusive
    ports = range(60100, 60111)
    proxy_url = _check_proxy_status(list(ports))
    logger.info(f"proxy is found, proxy url is:{proxy_url}")
    return proxy_url


class Client:
    @classmethod
    def reload(cls):
        cls._instance = None

    def __new__(cls):
        if not getattr(cls, "_instance", None):
            cfg = load_config()
            authentication_policy = None
            if cfg.auth and cfg.auth.client_id and cfg.auth.token_endpoint and cfg.auth.client_secret:
                authentication_policy = BearerTokenCredentialPolicy(
                    credential=MachineTokenCredential(
                        client_id=cfg.auth.client_id,
                        client_secret=cfg.auth.client_secret,
                        auth_endpoint=cfg.auth.token_endpoint,
                        scopes=cfg.auth.scopes,
                    ),
                    scopes=cfg.auth.scopes,
                )
            else:
                if not os.getenv("LSEG_ANALYTICS_PROXY_DISABLED"):
                    Client.retrieve_proxy_endpoint(cfg)

            logging_policy = NetworkTraceLoggingPolicy()
            logging_policy.enable_http_logger = True
            cls._instance = AnalyticsAPIClient(
                endpoint=cfg.base_url,
                username=cfg.username,
                authentication_policy=authentication_policy,
                logging_policy=logging_policy,
            )
            if cfg.headers:
                for key, value in cfg.headers.items():
                    cls._instance._config.headers_policy.add_header(key, value)
        return cls._instance

    @staticmethod
    def retrieve_proxy_endpoint(cfg):
        cfg.base_url = _get_proxy_info()
