import json

from .hik_dataclasses import HikDevice
from .hik_error import HikDeviceGatewayError


class HikDGDeviceManagement:

    def list_devices(self):
        raw = '''{
            "SearchDescription": {
                "position": 0,
                "maxResult": 100
            }
        }'''
        json_body = json.loads(raw)
        response = self.json_query("POST", self.baseurl + "/ISAPI/ContentMgmt/DeviceMgmt/deviceList?format=json", json_body)

        if 'statusString' in response:
            raise HikDeviceGatewayError(response['statusString'])

        if 'SearchResult' not in response:
            raise HikDeviceGatewayError("'SearchResult' missing from response body.")

        response = response['SearchResult']

        if 'numOfMatches' not in response:
            raise HikDeviceGatewayError("'numOfMatches' missing from response body.")

        if response['numOfMatches'] == 0:
            return []

        if 'MatchList' not in response:
            raise HikDeviceGatewayError("'MatchList' missing from response body.")

        if not isinstance(response['MatchList'], list):
            raise HikDeviceGatewayError("'MatchList' is not a list.")

        device_list = []
        for entry in response['MatchList']:
            if 'Device' in entry:
                device_list.append(HikDevice(entry['Device']))

        return device_list
