import argparse
import json
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse
from tolik_bot.view import (
    all_devices_state,
    get_usb_state,
    device_info,
    switch_usb_device,
    devices_cleanup
)
from tolik_bot.schemas import DeviceOut, DeviceState


app = FastAPI()


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}

    for error in exc_json:
        response['message'].append(error['loc'][-1] + f": {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/")
async def get_device_info():
    """Информация о Raspberry PI"""
    return device_info()


@app.get("/smart_switch/devices", response_model=list[DeviceOut], status_code=200)
async def all_devices_list():
    """Получение списка всех устройств"""
    return all_devices_state()


@app.post("/smart_switch/devices/", status_code=200)
async def all_devices_cleanup():
    """Сброс всех устройств в начальное состояние, успешный ответ FALSE"""
    return devices_cleanup()


@app.get("/smart_switch/devices/{device_name}", response_model=DeviceOut, status_code=200)
async def get_device_state(device_name: DeviceState = Depends(DeviceState)):
    """Получение статуса одного устройства"""
    usb = device_name.device_name
    return get_usb_state(usb)


@app.post("/smart_switch/devices/{device_name}/on", response_model=DeviceOut, status_code=200)
async def device_on(device: DeviceState = Depends(DeviceState), exclusive: Optional[bool] = None):
    """
    Включение устройства. Если exclusive=True остальные устройства отключаются
    """
    usb = device.device_name
    return switch_usb_device(device_name=usb, on=True, exclusive=exclusive)


@app.post("/smart_switch/devices/{device_name}/off", response_model=DeviceOut, status_code=200)
async def device_off(device: DeviceState = Depends(DeviceState)):
    """Выключение устройства"""
    usb = device.device_name
    return switch_usb_device(device_name=usb, on=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Bind host")
    parser.add_argument("-l", "--loglevel", type=str, default="info", help="Logging level")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Bind port")
    parser.add_argument("-r", "--reload", action="store_true", help="Reload when files change")
    args = parser.parse_args()
    uvicorn.run("tolik_bot.main:app",
                host=args.host, port=args.port, reload=args.reload, log_level=args.loglevel.lower())


if __name__ == "__main__":
    sys.exit(main())
