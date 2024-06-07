from copy import deepcopy

from tolik_bot.logger import get_logger

from tolik_bot.schemas import DeviceOut, device_usb_dict


logger = get_logger(__name__)

try:
    import RPi.GPIO as GPIO
except Exception as e:
    logger.warning(f"Failed to setup RPi.GPIO. Using Mock.GPIO. Error: ({e.__class__.__name__}) {e}")
    import Mock.GPIO as GPIO


def get_channel_number_by_device_name(device_name: str) -> int:
    return device_usb_dict[device_name]


def setup_device_to_bsm_mode():
    """
    Config device in BCM (channel numbering) mode
    and off device not needed warnings
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)


def device_info() -> dict:
    return GPIO.RPI_INFO


def all_devices_state() -> list[DeviceOut]:
    usb_list = []
    setup_device_to_bsm_mode()  # Setup channel
    for device_name, usb_pin in device_usb_dict.items():
        GPIO.setup(usb_pin, GPIO.OUT)
        usb_list.append(
            DeviceOut(
                device_name=device_name,
                on=bool(GPIO.input(usb_pin))
            )
        )
    return usb_list


def get_usb_state(device_name: str) -> DeviceOut:

    setup_device_to_bsm_mode()
    usb = get_channel_number_by_device_name(device_name)
    GPIO.setup(usb, GPIO.OUT)  # Setup usb channel
    state = bool(GPIO.input(usb))  # Returns 0 if OFF or 1 if ON

    logger.info(f'{device_name} - state "ON": {"ON" if state else "OFF"}')

    return DeviceOut(
        device_name=device_name,
        on=state
    )


def switch_usb_device(
        device_name: str,
        on: bool,
        exclusive: bool = False) -> DeviceOut:

    setup_device_to_bsm_mode()
    usb = get_channel_number_by_device_name(device_name)
    GPIO.setup(usb, GPIO.OUT)  # Setup usb channel
    if on:
        GPIO.output(usb, GPIO.HIGH)  # switch ON
        logger.info(f'Device {device_name} turn ON')
        if exclusive:
            device_usb_dict_to_off = deepcopy(device_usb_dict)
            device_usb_dict_to_off.pop(device_name)
            for usb_device_name in device_usb_dict_to_off:
                usb = get_channel_number_by_device_name(usb_device_name)
                GPIO.setup(usb, GPIO.OUT)
                GPIO.output(usb, GPIO.LOW)
    else:
        GPIO.output(usb, GPIO.LOW)  # switch OFF
        logger.info(f'Device {device_name} turn OFF')

    return DeviceOut(
        device_name=device_name,
        on=bool(GPIO.input(usb))
    )


def devices_cleanup() -> bool:
    setup_device_to_bsm_mode()

    return bool(GPIO.cleanup())
