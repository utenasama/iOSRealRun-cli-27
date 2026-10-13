# SPDX-License-Identifier: MPL-2.0
# GPL-3.0-or-later combination: see LICENSING.md.
"""iOS 17+ route playback with automatic DDI preparation and cleanup."""
import argparse
import asyncio
import logging
import math
import os

import coloredlogs
from pymobiledevice3.exceptions import AlreadyMountedError
from pymobiledevice3.services.dvt.instruments.device_info import DeviceInfo
from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.services.mobile_image_mounter import (
    MobileImageMounterService, auto_mount, image_type_for_device,
)

import config
import run
from driver import location
from init import init, route, tunnel

logger = logging.getLogger(__name__)


def positive_float(value):
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise argparse.ArgumentTypeError("必须为有限正数")
    return result


def positive_int(value):
    result = int(value)
    if result < 1:
        raise argparse.ArgumentTypeError("必须为正整数")
    return result


def parser():
    result = argparse.ArgumentParser(description="iOS 路线模拟（退出时恢复定位）")
    mode = result.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="检查开发者镜像及定位服务，不修改定位")
    mode.add_argument("--prepare", action="store_true", help="准备开发者镜像并检查连接，不模拟路线")
    mode.add_argument("--clear", action="store_true", help="清除模拟定位")
    result.add_argument("--duration", type=positive_float, help="运行秒数；省略则按圈数或无限循环")
    result.add_argument("--laps", type=positive_int, help="运行圈数")
    result.add_argument("--speed", type=positive_float, help="速度（m/s），默认读取 config.yaml")
    result.add_argument("--route", help="路线文件，相对路径以项目目录为基准")
    result.add_argument("--udid", help="指定 USB 设备")
    result.add_argument("--no-random", action="store_true", help="关闭路线及速度随机变化")
    return result


async def run_with_cleanup(simulation, points, speed, **options):
    try:
        return await run.run(simulation, points, speed, **options)
    finally:
        try:
            await location.clear_location(simulation)
        except BaseException:
            logger.error("清除定位失败，请重新连接后运行 main.py --clear；必要时重启手机")
            raise
        logger.info("已发送清除模拟定位命令")


async def main(args):
    # Validate the route before making any device changes.
    playback = not (args.check or args.prepare or args.clear)
    points = route.get_route(args.route) if playback else None
    speed = args.speed if args.speed is not None else float(config.config.v)
    if playback and (not math.isfinite(speed) or speed <= 0):
        raise ValueError("config.yaml 中的速度必须为有限正数")

    device = await asyncio.wait_for(init.init(args.udid), timeout=20)
    logger.info("已连接 %s，iOS %s，开发者模式已开启", device.product_type, device.version)
    async with tunnel.tunnel(device.serial) as rsd:
        async with MobileImageMounterService(rsd) as mounter:
            mounted = await asyncio.wait_for(
                mounter.is_image_mounted(image_type_for_device(rsd)), timeout=15,
            )
        if not mounted:
            if args.check or args.clear:
                raise RuntimeError("开发者镜像未就绪，请先运行 main.py --prepare")
            logger.info("正在下载并准备开发者镜像，首次运行可能需要几分钟")
            try:
                await asyncio.wait_for(auto_mount(rsd), timeout=600)
            except AlreadyMountedError:
                pass
            logger.info("开发者镜像已就绪")

        async with DvtProvider(rsd) as dvt:
            if args.check or args.prepare:
                async with DeviceInfo(dvt) as info:
                    await asyncio.wait_for(info.ls("/"), timeout=15)
                async with LocationSimulation(dvt):
                    logger.info("DVT 连接和定位服务检查通过")
                return
            async with LocationSimulation(dvt) as simulation:
                if args.clear:
                    await location.clear_location(simulation)
                    logger.info("已发送清除模拟定位命令")
                    return
                logger.info("开始模拟路线：%s 个点，速度约 %.2f m/s；Ctrl+C 退出并恢复定位", len(points), speed)
                updates = await run_with_cleanup(
                    simulation, points, speed, duration=args.duration,
                    laps=args.laps, randomize=not args.no_random,
                )
                logger.info("模拟结束，共发送 %s 次定位更新", updates)


def cli():
    args = parser().parse_args()
    debug = os.environ.get("DEBUG", "").lower() in {"1", "true", "yes"}
    coloredlogs.install(level=logging.DEBUG if debug else logging.INFO)
    logging.getLogger("pytcp").setLevel(logging.WARNING)
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        logger.info("已停止")
    except Exception as exc:
        logger.error("%s: %s", type(exc).__name__, exc)
        if debug:
            logger.exception("详细错误")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
