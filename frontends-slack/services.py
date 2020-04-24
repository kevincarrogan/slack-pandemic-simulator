import logging
import requests

logger = logging.getLogger("events")


def service_request(service_name, endpoint, payload):
    logger.debug(
        "service_request: %s %s %s", service_name, endpoint, payload,
    )

    schema = "http"
    service_prefix = "services-"
    url = f"{schema}://{service_prefix}{service_name}{endpoint}"

    requests.post(
        url, json=payload,
    )
