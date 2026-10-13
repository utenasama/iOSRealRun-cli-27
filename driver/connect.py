# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
"""USB discovery and pairing for the async pymobiledevice3 API."""
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.usbmux import list_devices


async def get_usbmux_lockdownclient(serial=None):
    devices = [device for device in await list_devices() if device.is_usb]
    if serial is not None:
        devices = [device for device in devices if device.matches_udid(serial)]
    if not devices:
        raise RuntimeError("未发现 USB 设备，请连接手机、解锁并信任此电脑")
    if len(devices) != 1:
        raise RuntimeError("请只连接一台手机，或用 --udid 指定设备")
    return await create_using_usbmux(
        serial=devices[0].serial, connection_type="USB", pair_timeout=15,
    )
