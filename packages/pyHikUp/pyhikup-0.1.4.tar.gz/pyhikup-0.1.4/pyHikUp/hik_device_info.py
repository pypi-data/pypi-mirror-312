import json

from .hik_dataclasses import HikDevice, HikDeviceInfo
from .hik_error import HikDeviceGatewayError


class HikDGDeviceInfo:

    def get_info(self, hikDevice: HikDevice):

        response = self.json_query("GET", self.baseurl +
                                   f"/ISAPI/System/deviceInfo?format=json&devIndex={hikDevice.devIndex}")

        if "DeviceInfo" not in response:
            raise HikDeviceGatewayError("Device Info Not Found")

        return HikDeviceInfo(response["DeviceInfo"])