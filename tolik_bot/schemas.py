from typing import Optional

from pydantic import BaseModel, validator

# Config USB devices
device_usb_dict = {
    'usb0': 23,
    'usb1': 17
}


class DeviceState(BaseModel):
    device_name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "device_name": 'usb0',
            }
        }

    @validator('device_name')
    def device_name_validator(cls, device_name):
        if device_name not in device_usb_dict:
            raise ValueError('Invalid usb name')
        return device_name


class DeviceOut(BaseModel):
    device_name: Optional[str] = None
    on: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "device_name": 'usb0',
                "on": True
            }
        }
