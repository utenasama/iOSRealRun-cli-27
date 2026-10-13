# iOSRealRun-cli-27

通过 USB 连接 iPhone，在开发者定位服务中播放路线。此版本将 iOSRealRun 的连接、隧道和定位调用迁移到 `pymobiledevice3 11.29.0` 异步 API，并加入开发者镜像自动准备、限时运行和退出清理。

**原创作者：Geniucker；原项目：[iOSRealRun/iOSRealRun-cli-17](https://github.com/iOSRealRun/iOSRealRun-cli-17)。** 本次适配从 [Preisthe/iOSRealRun-cli-17](https://github.com/Preisthe/iOSRealRun-cli-17) 的 `main` 分支继续开发，保留原始提交历史。当前仓库由 [utenasama](https://github.com/utenasama) 发布和维护，属于衍生适配版本。详细来源、改动范围及许可见 [NOTICE.md](NOTICE.md) 和 [LICENSING.md](LICENSING.md)。

已在 **macOS arm64 + iPhone 16 Pro + iOS 27.0.1** 上验证开发者镜像挂载、DVT 连接、短时定位更新和 Ctrl+C 清理。该结果证明开发者接口调用成功；地图显示、第三方应用距离/步数/记录结果尚未验证。iPhone 16 标准版及其他系统版本不能直接视为已验证，见 [验证记录](docs/VERIFICATION.md)。

## 环境要求

- 已安装 Git 和 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install)。推荐 Python 3.11。
- 当前实机验证平台为 macOS Apple Silicon。Windows、Linux 和 Intel Mac 尚未完成本版本实机验证。
- 程序要求 iOS 17 或更新版本，并开启开发者模式；实际兼容性取决于设备、系统版本和 pymobiledevice3。
- 使用支持数据传输的 USB 线，解锁手机，在 Mac 和 iPhone 上确认配件连接及“信任此电脑”提示。
- 首次准备需联网下载开发者镜像并请求 Apple 签名。本版本已验证的 macOS 用户态隧道流程无需 `sudo`。

## 安装

在终端中执行（若 `conda` 不可用，请先完成 Miniconda 的 shell 初始化并重新打开终端）：

```bash
git clone https://github.com/utenasama/iOSRealRun-cli-27.git
cd iOSRealRun-cli-27
conda create -n iosrealrun-ios27 --override-channels -c conda-forge python=3.11 pip -y
conda activate iosrealrun-ios27
python -m pip install -r requirements.lock.txt
python -m pip check
```

`requirements.lock.txt` 锁定此次验证的全部 Python 包版本。若其他平台无法安装其中的平台依赖，可改用 `python -m pip install -r requirements.txt`，并重新验证。`requirements.txt` 锁定直接依赖，间接依赖由 pip 解析。

也可以使用环境定义文件：

```bash
conda env create -f environment.yml
conda activate iosrealrun-ios27
```

若 Conda 插件仍提示默认源条款或源配置问题，使用上面的 `--override-channels -c conda-forge` 安装方式。两种方式任选一种创建环境。

macOS arm64 可按此次 Conda 包清单重建底层环境，再安装 Python 包：

```bash
conda create -n iosrealrun-ios27 --file conda-osx-arm64.lock.txt -y
conda activate iosrealrun-ios27
python -m pip install -r requirements.lock.txt
```

`conda-osx-arm64.lock.txt` 仅用于 macOS arm64，不包含全部 pip 包。`*-legacy.*` 和 `constraints-legacy.txt` 仅用于复现上游旧环境；当前代码需要新版异步 API，不能在旧环境直接运行。

## 首次连接

1. 在手机“设置 → 隐私与安全性 → 开发者模式”中开启开发者模式，并按系统提示重启和确认。
2. 用数据线连接电脑，解锁手机并信任此电脑。建议先只连接一台设备。
3. 准备开发者镜像并检查服务：

```bash
conda activate iosrealrun-ios27
python main.py --prepare
python main.py --check
```

`--prepare` 在需要时下载并挂载开发者镜像，同时检查 DVT 和定位通道；`--check` 检查已有镜像和服务。这两个模式不会设置模拟坐标。手机重启后可能需要重新准备。普通路线播放也会在镜像缺失时自动准备。

## 路线与速度

编辑 `config.yaml`，主要配置为：

```yaml
v: 3.3
routeConfig: HNroute.txt
```

`v` 为米/秒，3.3 m/s 约等于 11.88 km/h。旧配置中的 `libimobiledeviceDir`、`imageDir` 保留用于对照，当前连接流程不读取它们。

路线文件是逗号分隔的坐标对象，至少两个点；不需要外层方括号。例如：

```text
{"lng":"120.7330","lat":"30.5280"},
{"lng":"120.7340","lat":"30.5290"},
{"lng":"120.7335","lat":"30.5295"}
```

输入坐标按上游的 **BD-09** 规则转换为 WGS84。不要直接把 WGS84/GPX 坐标当作 BD-09 输入。附带的 `HNroute.txt` 是上游示例路线；使用前请检查并换成适合自己的测试路线。程序将末点连回起点形成一圈，相对路径以项目目录为基准，绝对路径也可用。坐标转换保留上游实现，精度和中国境外适用性未单独验证。

## 运行

```bash
# 建议先做短时测试，正常结束时发送清除定位命令
python main.py --duration 30

# 持续循环，按 Ctrl+C 停止
python main.py

# 跑一圈，指定速度和路线
python main.py --laps 1 --speed 3.3 --route HNroute.txt

# 固定路线和速度，关闭随机变化
python main.py --duration 30 --no-random
```

默认保留上游的速度和路线随机变化。更新按约 0.2 秒的目标间隔异步发送，服务响应时间可能影响实际间隔。`--duration` 约束路线播放时长，不包含连接及镜像准备时间，超时处理和清理也需要时间。插值会先构建整圈坐标，极长路线或极低速度会增加内存和准备时间。

| 参数 | 含义 |
| --- | --- |
| `--prepare` | 准备镜像并检查连接，不播放路线 |
| `--check` | 检查现有镜像、DVT 和定位通道 |
| `--clear` | 发送清除模拟定位命令 |
| `--duration 秒数` | 限时播放，要求有限正数 |
| `--laps 圈数` | 指定正整数圈数；与时长同时设置时，以先达到的限制为准 |
| `--speed 米/秒` | 覆盖配置速度，要求有限正数 |
| `--route 路径` | 覆盖配置中的路线文件 |
| `--udid 标识` | 多台 USB 设备时指定一台；不要把设备标识公开到 Issue |
| `--no-random` | 关闭速度和路线随机变化 |
| `--help` | 查看命令帮助 |

`--prepare`、`--check`、`--clear` 互斥。播放参数在这三个模式下不用于播放。成功退出码为 0，普通错误为 1；Ctrl+C 正常处理后退出码为 0。

## 停止与恢复定位

正常结束、Ctrl+C 或更新异常时，程序在关闭服务前尝试清除模拟定位。清理失败会明确报错。强制杀进程、断电或拔线可能使清理无法完成；重新连接并解锁后执行：

```bash
python main.py --clear
```

若提示镜像未就绪，先运行 `python main.py --prepare`。如果手机仍未恢复实际定位，请重启手机。日志中的“已发送清除模拟定位命令”表示服务调用完成，实际显示仍应在手机上确认。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| 找不到 USB 设备 | 确认数据线、解锁、信任提示；检查 Finder 是否识别手机，重新插拔后再试 |
| 找到多台设备 | 只连接一台，或用 `--udid` 指定设备 |
| 开发者模式未开启 | 在手机设置中开启，完成重启及确认 |
| 开发者镜像未就绪 | 运行 `--prepare`，确认网络能访问镜像下载和 Apple 签名服务 |
| 隧道或 DVT 连接失败/超时 | 保持手机解锁，重连 USB，重试 `--prepare` 和 `--check`；记录准确的系统及依赖版本 |
| 安装失败、找不到包版本 | 检查 Python 版本及包索引镜像；必要时使用 `python -m pip install --index-url https://pypi.org/simple -r requirements.txt` |
| 路线解析失败 | 检查对象格式、至少两个点、经纬度范围及有限数值 |
| 应用内没有距离或步数 | 开发者定位不等同于运动传感器数据，应用是否采用坐标需单独验证 |

查看错误细节：`DEBUG=1 python main.py --check`。提交日志前删去 UDID、序列号、配对信息、个人路线和其他隐私数据。

## 开发与验证

```bash
python -m pip check
python -m unittest discover -s tests -v
```

目前 7 项自动测试覆盖时长控制、事件循环调度、更新失败/取消清理、清理失败报告、坏路线在连接前拒绝和隧道打开失败的资源释放。自动测试使用模拟服务，无需连接 iPhone；实机记录见 [docs/VERIFICATION.md](docs/VERIFICATION.md)。

| 文件 | 作用 |
| --- | --- |
| `main.py` | 命令参数、镜像准备、DVT 会话及退出清理 |
| `driver/` | USB 发现和定位设置/清除 |
| `init/` | 设备检查、隧道管理和路线加载 |
| `run.py` | 上游坐标转换、插值与随机变化，以及异步播放 |
| `util/route.py` | 路线解析和坐标校验 |
| `tests/` | 无设备自动测试 |

相关文档：[pymobiledevice3 Python API](https://doronz88.github.io/pymobiledevice3/guides/python-api/)、[iOS 17+ 隧道](https://doronz88.github.io/pymobiledevice3/guides/ios17-tunnels/)、[CLI recipes](https://doronz88.github.io/pymobiledevice3/guides/cli-recipes/)。

## 作者、许可与使用范围

保留原创作者 Geniucker、iOSRealRun 项目及所有原贡献者的归属；Preisthe 是直接克隆来源。此次维护内容为 iOS 27 环境适配、异步 API 迁移、参数、清理逻辑、测试和文档，详见 [NOTICE.md](NOTICE.md)。本版本没有原作者或 Apple 的官方背书。

上游 MPL-2.0 全文原样保留在 [LICENSE](LICENSE)。由于运行依赖 `pymobiledevice3 11.29.0` 为 GPL-3.0-or-later，本版本依据 MPL 2.0 第 3.3 条，在与该依赖组成 Larger Work 时，同时按 GPL-3.0-or-later 提供 MPL 受保护源码；组合程序按 GPL-3.0-or-later 分发。GPL 文本见 [COPYING](COPYING)，具体范围与第三方依赖说明见 [LICENSING.md](LICENSING.md)。

面向自有或获授权设备的定位开发与测试。使用时应遵守适用法律及目标应用/服务的规则。项目不承诺第三方平台认可模拟记录，也不提供绕过平台校验的能力；此使用说明不增加或限制开源许可证授予的权利。
