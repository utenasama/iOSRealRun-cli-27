# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import main
from init import tunnel
from util.route import parse_route


POINTS = [{"lat": 30.528, "lng": 120.733}, {"lat": 30.529, "lng": 120.734}]


class PlaybackTests(unittest.IsolatedAsyncioTestCase):
    async def test_duration_yields_to_event_loop_and_clears(self):
        simulation = AsyncMock()
        heartbeat = asyncio.Event()
        asyncio.get_running_loop().call_later(0.01, heartbeat.set)
        updates = await main.run_with_cleanup(
            simulation, POINTS, 3.3, duration=0.05, randomize=False,
        )
        self.assertTrue(heartbeat.is_set())
        self.assertGreater(updates, 0)
        self.assertEqual(simulation.set.await_count, updates)
        simulation.clear.assert_awaited_once()

    async def test_cancel_during_location_update_still_clears(self):
        started = asyncio.Event()

        async def stalled_update(*args):
            started.set()
            await asyncio.Event().wait()

        simulation = AsyncMock()
        simulation.set.side_effect = stalled_update
        task = asyncio.create_task(main.run_with_cleanup(simulation, POINTS, 3.3))
        await asyncio.wait_for(started.wait(), 1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        simulation.clear.assert_awaited_once()

    async def test_location_error_still_clears_and_propagates(self):
        simulation = AsyncMock()
        simulation.set.side_effect = RuntimeError("connection lost")
        with self.assertRaisesRegex(RuntimeError, "connection lost"):
            await main.run_with_cleanup(simulation, POINTS, 3.3)
        simulation.clear.assert_awaited_once()

    async def test_cleanup_failure_is_not_reported_as_success(self):
        simulation = AsyncMock()
        simulation.clear.side_effect = RuntimeError("clear failed")
        with self.assertLogs(main.logger, level="ERROR"):
            with self.assertRaisesRegex(RuntimeError, "clear failed"):
                await main.run_with_cleanup(
                    simulation, POINTS, 3.3, duration=0.01, randomize=False,
                )

    async def test_bad_route_fails_before_device_connection(self):
        args = main.parser().parse_args(["--route", "tests/nonexistent-route.txt"])
        with patch.object(main.init, "init", new_callable=AsyncMock) as connect:
            with self.assertRaises(FileNotFoundError):
                await main.main(args)
            connect.assert_not_awaited()

    async def test_failed_tunnel_open_closes_handle(self):
        handle = AsyncMock()
        handle.aopen.side_effect = TimeoutError("connect failed")
        with patch.object(tunnel, "PreferredRsdTunnel", return_value=handle):
            with self.assertRaises(TimeoutError):
                async with tunnel.tunnel():
                    self.fail("a failed connection must not yield a tunnel")
        handle.aclose.assert_awaited_once()

    def test_rejects_short_or_nonfinite_routes(self):
        with self.assertRaises(ValueError):
            parse_route('{"lat": "30", "lng": "120"}')
        with self.assertRaises(ValueError):
            parse_route('{"lat": "nan", "lng": "120"}, {"lat": "30", "lng": "120"}')


if __name__ == "__main__":
    unittest.main()
