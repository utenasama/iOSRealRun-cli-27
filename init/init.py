# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
"""Check the connected device without changing its settings."""
from dataclasses import dataclass

from driver import connect


@dataclass(frozen=True)
class Device:
    serial: str
    product_type: str
    version: str


async def init(serial=None):
    async with await connect.get_usbmux_lockdownclient(serial) as lockdown:
        version = lockdown.product_version
        if int(version.split(".")[0]) < 17:
            raise RuntimeError("本项目需要 iOS 17 或更高版本")
        if not await lockdown.get_developer_mode_status():
            raise RuntimeError("请在手机的 设置 → 隐私与安全性 中开启开发者模式")
        return Device(lockdown.udid, lockdown.all_values["ProductType"], version)
