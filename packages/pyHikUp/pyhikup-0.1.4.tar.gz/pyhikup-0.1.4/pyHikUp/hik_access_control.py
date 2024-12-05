import base64
import json
import os
import uuid
from datetime import datetime
import filetype
from dateutil.relativedelta import relativedelta

from .hik_dataclasses import HikDevice
from .hik_error import HikDeviceGatewayError


class HikAccessControl:

    def check_employee_exists(self, device: HikDevice, employee_num):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
                    "UserInfoSearchCond": {
                        "searchID": "C7E71364-4560-0001-6EDD-16ED17B01CCD",
                        "searchResultPosition": 0,
                        "maxResults": 1,
                        "employeeNo": "123456"
                    }
                }'''
        json_body = json.loads(raw)
        json_body['UserInfoSearchCond']['searchID'] = str(uuid.uuid4())
        json_body['UserInfoSearchCond']['employeeNo'] = employee_num

        url_path_params = f"/ISAPI/AccessControl/UserInfo/Search?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'errorMsg' in response:
            raise HikDeviceGatewayError(response['errorMsg'])

        if 'UserInfoSearch' not in response:
            raise HikDeviceGatewayError("'UserInfoSearch' missing from response body.")

        if 'responseStatusStrg' in response['UserInfoSearch']:
            if response['UserInfoSearch']['responseStatusStrg'] == 'NO MATCH':
                return []

        if response['UserInfoSearch']['numOfMatches'] < 1:
            return []

        if 'UserInfo' not in response['UserInfoSearch']:
            raise HikDeviceGatewayError("'UserInfo' missing from response body.")

        if not isinstance(response['UserInfoSearch']['UserInfo'], list):
            raise HikDeviceGatewayError("'UserInfo' is not a list.")

        if len(response['UserInfoSearch']['UserInfo']) < 1:
            return False

        return True

    def get_employee_num_list(self, device: HikDevice, offset=0, max_results=2000):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
            "UserInfoSearchCond": {
                "searchID": "C7E71364-4560-0001-6EDD-16ED17B01CCD",
                "searchResultPosition": 0,
                "maxResults": 9999
            }
        }'''

        json_body = json.loads(raw)
        json_body['UserInfoSearchCond']['searchID'] = str(uuid.uuid4())
        json_body['UserInfoSearchCond']['searchResultPosition'] = offset
        json_body['UserInfoSearchCond']['maxResults'] = max_results

        url_path_params = f"/ISAPI/AccessControl/UserInfo/Search?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'errorMsg' in response:
            raise HikDeviceGatewayError(response['errorMsg'])

        if 'UserInfoSearch' not in response:
            raise HikDeviceGatewayError("'UserInfoSearch' missing from response body.")

        if 'responseStatusStrg' in response['UserInfoSearch']:
            if response['UserInfoSearch']['responseStatusStrg'] == 'NO MATCH':
                return []

        if response['UserInfoSearch']['numOfMatches'] < 1:
            return []

        if 'UserInfo' not in response['UserInfoSearch']:
            raise HikDeviceGatewayError("'UserInfo' missing from response body.")

        if not isinstance(response['UserInfoSearch']['UserInfo'], list):
            raise HikDeviceGatewayError("'UserInfo' is not a list.")

        if len(response['UserInfoSearch']['UserInfo']) < 1:
            return []

        employee_num_list = []
        for employee in response['UserInfoSearch']['UserInfo']:
            employee_num_list.append(employee['employeeNo'])

        return employee_num_list

    def add_person(self, device: HikDevice, employee_num: str, name: str,
                   begin_time: datetime = None, end_time: datetime = None,
                   user_type: str = "normal"):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")
        if user_type != 'normal' and user_type != 'visitor':
            raise HikDeviceGatewayError("Unknown user_type")
        if begin_time is not None and end_time is not None:
            # Dates cannot be the same.
            if (begin_time.replace(second=0, microsecond=0).isoformat()
                    == end_time.replace(second=0, microsecond=0).isoformat()):
                raise HikDeviceGatewayError('Begin and End DateTimes cannot be the same.')
        if begin_time is not None and end_time is None:
            end_time = begin_time + relativedelta(years=5)
        if begin_time is None and end_time is not None:
            begin_time = datetime.now()
        if end_time is not None:
            if end_time.year > 2037:
                end_time = end_time.replace(year=2037)

        raw = '''{
            "UserInfo": [
                {
                    "employeeNo": "",
                    "name": "",
                    "userType": "normal",
                    "Valid": {
                        "beginTime": "2024-01-01T00:00:00",
                        "endTime": "2037-12-31T23:59:59"
                    }
                }
            ]
        }'''
        json_body = json.loads(raw)
        json_body['UserInfo'][0]['employeeNo'] = employee_num
        json_body['UserInfo'][0]['name'] = name
        json_body['UserInfo'][0]['userType'] = user_type
        if begin_time is not None and end_time is not None:
            json_body['UserInfo'][0]['Valid']['beginTime'] = begin_time.replace(second=0, microsecond=0).isoformat()
            json_body['UserInfo'][0]['Valid']['endTime'] = end_time.replace(second=0, microsecond=0).isoformat()

        url_path_params = f"/ISAPI/AccessControl/UserInfo/Record?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'errorMsg' in response:
            raise HikDeviceGatewayError(response['errorMsg'])

        if 'UserInfoOutList' not in response:
            raise HikDeviceGatewayError("'UserInfoOutList' missing from response body.")

        if 'UserInfoOut' not in response['UserInfoOutList']:
            raise HikDeviceGatewayError("'UserInfoOut' missing from response body.")

        if not isinstance(response['UserInfoOutList']['UserInfoOut'], list):
            raise HikDeviceGatewayError("'UserInfoOut' is not a list.")

        if len(response['UserInfoOutList']['UserInfoOut']) == 0:
            return []

        if 'statusCode' not in response['UserInfoOutList']['UserInfoOut'][0]:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['UserInfoOutList']['UserInfoOut'][0]['statusCode'] != 1:
            if 'errorMsg' in response['UserInfoOutList']['UserInfoOut'][0]:
                raise HikDeviceGatewayError(response['UserInfoOutList']['UserInfoOut'][0]['errorMsg'])
            else:
                raise HikDeviceGatewayError(
                    f"Error - StatusCode: {str(response['UserInfoOutList']['UserInfoOut'][0]['statusCode'])}")

        return True

    def delete_person(self, device: HikDevice, employee_num: str):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
            "UserInfoDetail": {
                "mode": "byEmployeeNo",
                "EmployeeNoList": [
                    {
                        "employeeNo": "123456"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['UserInfoDetail']['EmployeeNoList'][0]['employeeNo'] = employee_num

        url_path_params = f"/ISAPI/AccessControl/UserInfoDetail/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def add_card(self, device: HikDevice, employee_num: str, card_num: str):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
            "CardInfo": {
                "employeeNo": "123456",
                "cardNo": "1234567890"
            }
        }'''
        json_body = json.loads(raw)
        json_body['CardInfo']['employeeNo'] = employee_num
        json_body['CardInfo']['cardNo'] = card_num

        url_path_params = f"/ISAPI/AccessControl/CardInfo/Record?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def delete_card(self, device: HikDevice, card_num: str):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
            "CardInfoDelCond": {
                "CardNoList": [
                    {
                        "cardNo": "1234567890"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['CardInfoDelCond']['CardNoList'][0]['cardNo'] = card_num

        url_path_params = f"/ISAPI/AccessControl/CardInfo/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def add_face(self, device: HikDevice, employee_num: str,
                 face_img_filepath: str = None,
                 face_img_base64: str = None):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
                    "FaceInfo": {
                        "employeeNo": "123456"
                    }
                }'''

        json_body = json.loads(raw)
        json_body['FaceInfo']['employeeNo'] = employee_num

        files = None
        if face_img_filepath is not None:
            if not os.path.isfile(face_img_filepath):
                raise HikDeviceGatewayError(f'Failed to find {face_img_filepath}')

            if not filetype.is_image(face_img_filepath):
                raise HikDeviceGatewayError(f'{face_img_filepath} is not an image')

            files = {
                'data': (None, json.dumps(json_body).encode('ascii'), 'application/json'),
                'FaceDataRecord': (None, open(face_img_filepath, 'rb'), 'image/jpeg')
            }

        if face_img_base64 is not None:
            files = {
                'data': (None, json.dumps(json_body).encode('ascii'), 'application/json'),
                'FaceDataRecord': (None, base64.b64decode(face_img_base64.encode('ascii')), 'image/jpeg')
            }

        if files is None:
            raise HikDeviceGatewayError("Valid image not provided.")

        url_path_params = f"/ISAPI/Intelligent/FDLib/FaceDataRecord?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "POST",
            self.baseurl + url_path_params,
            None,
            files=files)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                if 'subStatusCode' in response:
                    raise HikDeviceGatewayError(f"{response['errorMsg']} - {response['subStatusCode']}")
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True

    def delete_face(self, device: HikDevice, employee_num: str):
        if device.devStatus == 'offline':
            raise HikDeviceGatewayError("Device is offline")

        raw = '''{
            "FaceInfoDelCond": {
                "EmployeeNoList": [
                    {
                        "employeeNo": "123456"
                    }
                ]
            }
        }'''
        json_body = json.loads(raw)
        json_body['FaceInfoDelCond']['EmployeeNoList'][0]['employeeNo'] = employee_num

        url_path_params = f"/ISAPI/Intelligent/FDLib/FDSearch/Delete?format=json&devIndex={device.devIndex}"
        response = self.json_query(
            "PUT",
            self.baseurl + url_path_params,
            json_body)

        if 'statusCode' not in response:
            raise HikDeviceGatewayError("'statusCode' missing from response body.")

        if response['statusCode'] != 1:
            if 'errorMsg' in response:
                raise HikDeviceGatewayError(response['errorMsg'])
            else:
                raise HikDeviceGatewayError(f"Error - StatusCode: {str(response['statusCode'])}")

        return True
