import logging
from collections import defaultdict
from dataclasses import dataclass, asdict

log = logging.getLogger(__name__)


class Observable:
    # A set of all attributes which get changed
    changed_attributes = set()

    def __init__(self):
        self.observed = defaultdict(list)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        for observer in self.observed.get(name, []):
            observer(name)

    def add_observer(self, name):
        self.observed[name].append(lambda name: self.changed_attributes.add(name))


def sanitise_args(obj: object, args, kwargs):
    kwarg_dict = dict()
    obj.changed_attributes = set()

    for arg in args:
        if isinstance(arg, dict):
            kwarg_dict.update(arg)

    for k, v in kwargs.items():
        if hasattr(type(obj), k):
            kwarg_dict[k] = v
            obj.changed_attributes.add(k)
        else:
            log.debug(f"{obj.__class__.__name__}.{k} - attribute ignored.")
            # raise ValueError(f"No such attribute: {k}")

    return kwarg_dict

@dataclass
class HikDeviceInfo:
    bootVersion: any = None
    deviceID: int = 0
    deviceName: str = ""
    deviceType: str = ""
    deviceDescription: str = ""
    encoderReleasedDate: str = ""
    encoderVersion: str = ""
    firmwareReleasedDate: str = ""
    firmwareVersion: str = ""
    hardwareVersion: str = ""
    macAddress: str = ""
    model: str = ""
    serialNumber: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        device_dict = sanitise_args(self, args, kwargs)

        for property_name in device_dict:
            if isinstance(device_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, device_dict[property_name])

    def dict(self):
        device_dict = {}
        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                device_dict[k] = v
            elif isinstance(v, type(None)):
                device_dict[k] = None
            else:
                device_dict[k] = str(v)

        return device_dict
@dataclass
class HikDevice:
    ISAPIParams: any = None
    activeStatus: bool = False
    devIndex: str = ""
    devMode: str = ""
    devName: str = ""
    devStatus: str = ""
    devType: str = ""
    devVersion: str = ""
    protocolType: str = ""
    videoChannelNum: int = -1,

    def __init__(self, *args, **kwargs):
        super().__init__()
        device_dict = sanitise_args(self, args, kwargs)

        for property_name in device_dict:
            if isinstance(device_dict[property_name], (str, type(None), bool, int)):
                setattr(self, property_name, device_dict[property_name])

            if isinstance(device_dict[property_name], dict):
                if property_name == "ISAPIParams":
                    self.ISAPIParams = device_dict[property_name]

    def dict(self):
        device_dict = {}
        for k, v in asdict(self).items():
            if isinstance(v, (list, dict, bool, int)):
                device_dict[k] = v
            elif isinstance(v, type(None)):
                device_dict[k] = None
            else:
                device_dict[k] = str(v)

        return device_dict
