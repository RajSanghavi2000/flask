import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .constants import INVALID_REQUEST_ERROR_MESSAGE
from .enum import HttpMethodEnum, RequestBodyType


def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=None, session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def invoke_request(endpoint, method, headers, payload=None, params=None, timeout=61, raise_timeout_exception=True,
                   files=dict(), request_type=RequestBodyType.RAW.value, status_force_list: tuple = (500, 502, 504),
                   retries=3, backoff_factor=0.3, verify=True):
    if params is None:
        params = {}
    if request_type == RequestBodyType.RAW.value:
        payload = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    _request = requests_retry_session(status_forcelist=status_force_list,
                                      retries=retries,
                                      backoff_factor=backoff_factor)
    _request.headers.update({
        **headers
    })
    try:
        response = None
        if method == HttpMethodEnum.GET.value:
            response = _request.get(url=endpoint, data=payload, params=params, timeout=timeout, files=files, verify=verify)
        if method == HttpMethodEnum.POST.value:
            response = _request.post(url=endpoint, data=payload, params=params, timeout=timeout, files=files, verify=verify)
        if method == HttpMethodEnum.PUT.value:
            response = _request.put(url=endpoint, data=payload, params=params, timeout=timeout, files=files, verify=verify)
        if method == HttpMethodEnum.DELETE.value:
            response = _request.delete(url=endpoint, data=payload, params=params, timeout=timeout, verify=verify)
        if method == HttpMethodEnum.PATCH.value:
            response = _request.patch(url=endpoint, data=payload, params=params, timeout=timeout, verify=verify)

        logging.info("API Response statistics: %s", {"endpoint": endpoint, "Time": response.elapsed.total_seconds()})
        return response.json(), response.status_code
    except ValueError:
        return response, response.status_code
    except requests.exceptions.ReadTimeout:
        if not raise_timeout_exception: return True
        raise
    except requests.exceptions.RequestException:
        logging.exception(INVALID_REQUEST_ERROR_MESSAGE.format(endpoint))
        raise


def download_file(endpoint, headers, timeout, bot_id):
    _request = requests_retry_session()
    _request.headers.update({
        **headers
    })
    try:
        response = _request.get(url=endpoint, timeout=timeout)
        return response.content, response.status_code
    except ValueError:
        logging.exception(INVALID_REQUEST_ERROR_MESSAGE.format(endpoint))

    except requests.exceptions.ReadTimeout:
        msg = "Service Call Error Bot_{}: Timeout while downloading {}".format(bot_id, endpoint)
        logging.exception(msg)

    except requests.exceptions.RequestException:
        logging.exception(INVALID_REQUEST_ERROR_MESSAGE.format(endpoint))
