import logging

logger = logging.getLogger("events")


def service_request(service_name, endpoint, payload):
    logger.debug(
        "service_request: %s %s %s", service_name, endpoint, payload,
    )
