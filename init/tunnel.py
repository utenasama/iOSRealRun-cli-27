# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
"""Manage one no-root tunnel in the same process as DVT."""
import asyncio
from contextlib import asynccontextmanager

from pymobiledevice3.remote.rsd_tunnel import PreferredRsdTunnel


@asynccontextmanager
async def tunnel(serial=None):
    handle = PreferredRsdTunnel(serial=serial)
    try:
        rsd = await asyncio.wait_for(handle.aopen(), timeout=30)
        yield rsd
    finally:
        await asyncio.wait_for(handle.aclose(), timeout=15)
