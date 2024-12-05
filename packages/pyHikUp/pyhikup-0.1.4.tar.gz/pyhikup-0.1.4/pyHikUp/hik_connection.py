import logging
import json
from json import JSONDecodeError
import requests
from requests.auth import HTTPDigestAuth

log = logging.getLogger(__name__)


class HikDGConnection:

    def __init__(self, url_components, user, pwd):
        self.ssl_context = None
        self.url_components = url_components
        self.user = user
        self.pwd = pwd
        if url_components['host'] == '':
            raise ValueError("Invalid Connection URL")
        if url_components['scheme'] == '':
            url_components['scheme'] = 'http'

        self.baseurl = f"{url_components['scheme']}://{url_components['host']}"
        if url_components['port']:
            self.baseurl = self.baseurl + f":{url_components['port']}"

        log.info(f"HikDevice Gateway BASE_URL: {self.baseurl}")

    def json_query(self, method, url, json_body: dict = '', headers=None, files=None):
        raw_body = ''
        if json_body:
            if not isinstance(json_body, dict):
                raise ValueError("Variable 'json_body' must be of type dict.")
            else:
                raw_body = json.dumps(json_body)

        headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        log.debug(f"Request data: host={self.baseurl}, {method}, {url}, {headers}, {raw_body}")

        if isinstance(files, dict):
            headers = None
            raw_body = None

        response = requests.request(method,
                                    url,
                                    data=raw_body,
                                    headers=headers,
                                    auth=HTTPDigestAuth(self.user, self.pwd),
                                    files=files)

        # Try to convert body into json
        try:
            json_body = json.loads(response.text)
        except JSONDecodeError:
            json_body = None
        except Exception as e:
            log.error(e)
            json_body = None

        return json_body


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
