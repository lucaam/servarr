#!/usr/local/bin/python3

import requests
import os
import logging
from json import JSONDecodeError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

PROWLARR_HOST = os.getenv("PROWLARR_HOST")
API_KEY = os.getenv("API_KEY")

def post(url: str, headers: dict, body: dict):
    """
    Handle POST requests towards an url, logging both
    the details before sending it and the response.

    Parameters
    ----------
    url : str
        HTTP request URL as string
    headers : dict
        HTTP headers to be used in the request
    body : dict
        Request body needed for the POST
    """

    logger.debug(" ".join([
        "POST",
        url,
        ", ".join([": ".join(header) for header in headers]),
        str(body)
    ]))

    response = requests.post(
        url=url,
        data=body,
        headers=headers
    )

    logger.debug(" ".join([
        "Status Code:",
        response.status_code,
        "Response body:",
        response.text
    ]))

    try:
        return {"code": response.status_code, "response": response.json()}
    except JSONDecodeError:
        return {"code": response.status_code, "response": response.text}
    
logger.info("Setup Flaresolverr tags in Prowlarr")

headers = {
    "content-type": "application/json",
    "x-api-key": API_KEY,
    "x-requested-with": "XMLHttpRequest"
}

body = {
    "label":"flare"
}

res = post(
    url="http://{}/api/v1/tag".format(PROWLARR_HOST),
    headers=headers,
    body=body
)

# TO-DO: Check for response status code and decide what to do

logger.info("Setup Radarr in Prowlarr")

headers = {
    "content-type": "application/json",
    "x-api-key": API_KEY,
    "x-requested-with": "XMLHttpRequest",
    "X-Prowlarr-Client": "true"
}

body = {
    "syncLevel": "fullSync",
    "fields": [
        {
            "name": "prowlarrUrl",
            "value": "http://servarr-prowlarr:9696"
        },
        {
            "name": "baseUrl",
            "value": "http://servarr-radarr:7878"
        },
        {
            "name": "apiKey",
            "value": API_KEY
        },
        {
            "name": "syncCategories",
            "value": [
                2000,
                2010,
                2020,
                2030,
                2040,
                2045,
                2050,
                2060,
                2070,
                2080,
                2090
            ]
        }
    ],
    "implementationName": "Radarr",
    "implementation": "Radarr",
    "configContract": "RadarrSettings",
    "infoLink": "https://wiki.servarr.com/prowlarr/supported#radarr",
    "tags": [],
    "name": "Radarr"
}

res = post(
    url="http://{}/api/v1/applications".format(PROWLARR_HOST),
    headers=headers,
    body=body
)

# TO-DO: Check for response status code and decide what to do