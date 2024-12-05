import logging
import validators

from .hik_access_control import HikAccessControl
from .hik_connection import HikDGConnection
from .hik_device_info import HikDGDeviceInfo
from .hik_device_management import HikDGDeviceManagement
from .hik_utils import url_parser


class HikDeviceGateway(HikDGConnection, HikDGDeviceManagement, HikAccessControl, HikDGDeviceInfo):

    def __init__(self, **kwargs):
        # Set default values if not present
        host = kwargs.get('host', "localhost")
        port = kwargs.get('port', None)
        url_components = url_parser(host)
        if url_components['host'] == '':
            url_components['host'] = url_components['path']
            url_components['path'] = ''
        if port:
            url_components['port'] = port
        user = kwargs.get('username', "admin")
        pwd = kwargs.get('password', "admin")

        super().__init__(url_components=url_components, user=user, pwd=pwd)
