import hashlib
import hmac
import requests
import json
from .config import API_URL, API_VERSION, API_VERSION2, API_METHODS
from .utils import verify_request
from requests.exceptions import HTTPError
from urllib.parse import urlencode


class IPy3CW:
    def request(self, entity: str, action: str = '', action_id: str = None, payload: any = None):
        pass


class Py3CW(IPy3CW):

    def __init__(self, key: str, secret: str):
        """
        Init the library with a 3commas key and secret strings. Get keys from your account API
        (https://3commas.io/api_access_tokens) page
        """

        if key is None or key == '':
            raise ValueError('Please enter a 3commas API key')
        if secret is None or secret == '':
            raise ValueError('Please enter a 3commas API secret')

        self.key = key
        self.secret = secret

    def __generate_signature(self, path: str, data: str) -> str:
        """
        Generates the signature needed for 3commas API communication
        """
        encoded_key = str.encode(self.secret)
        message = str.encode(path + data)
        signature = hmac.new(encoded_key, message, hashlib.sha256).hexdigest()
        return signature

    def __make_request(self, http_method: str, path: str, params: any, payload: any, timeout: int = 0):
        """
        Private method that makes the actual request. Returns the response in JSON format for both
        success and error responses.
        """
        
        apv = API_VERSION
        if "smart_trades" in path and not "smart_trades_v1" in path:
            apv = API_VERSION2
        else:
            path=path.replace("smart_trades_v1","smart_trades")
            
        if (params is not None and len(params) > 0):
            relative_url = f"{apv}{path}?{params}"
        else:
            relative_url = f"{apv}{path}"
            
        if (http_method == "GET" or (payload is not None and len(payload) == 0)):
            payload = None

        signature = self.__generate_signature(relative_url, (json.dumps(payload) if payload is not None else ''))
        try:
            request_url = f"{API_URL}{relative_url}"
            if timeout != 0:
                response = requests.request(
                    method=http_method,
                    url=request_url,
                    timeout=timeout,
                    headers={
                        'APIKEY': self.key,
                        'Signature': signature
                    },
                    json=payload
                )
            else:
                response = requests.request(
                    method=http_method,
                    url=request_url,
                    headers={
                        'APIKEY': self.key,
                        'Signature': signature
                    },
                    json=payload
                )

            response_json = json.loads(response.text)
            if type(response_json) is dict and 'error' in response_json:
                return response_json, None
            else:
                return None, response_json

        except HTTPError as http_err:
            return {'error': True, 'msg': 'HTTP error occurred: {0}'.format(http_err)}, None

        except Exception as err:
            return {'error': True, 'msg': 'Other error occurred: {0}'.format(err)}, None

    @verify_request
    def request(self, entity: str, action: str = '', action_id: str = None, action_sub_id: str = None, payload: any = None, timeout: int = 10):
        """
        Constructs the API Url and makes the request.
        """
        api = API_METHODS[entity][action]
        method, api_path = api
        api_path = api_path.replace('{id}', action_id or '')
        api_path = api_path.replace('{sub_id}', action_sub_id or '')

        if method == 'GET' and payload is not None:
            params = urlencode(payload)
        else:
            params = ''

        return self.__make_request(
            http_method=method,
            path='{entity}{separator}{api_path}'.format(
                entity=entity,
                separator='/' if api_path else '',
                api_path=api_path or ''
            ),
            params=params,
            payload=payload,
            timeout = timeout
        )
