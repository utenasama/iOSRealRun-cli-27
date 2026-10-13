# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
import asyncio

async def set_location(simulation, lat: float, lng: float):
    await asyncio.wait_for(simulation.set(lat, lng), timeout=10)

async def clear_location(simulation):
    await asyncio.wait_for(simulation.clear(), timeout=10)
