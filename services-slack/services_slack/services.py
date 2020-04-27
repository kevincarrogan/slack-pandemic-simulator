import requests


def service_request(service_name, endpoint, payload):
    schema = "http"
    service_prefix = "services-"
    url = f"{schema}://{service_prefix}{service_name}{endpoint}"

    return requests.post(url, json=payload).json()
