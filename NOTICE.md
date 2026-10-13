# 来源与改动说明

## 原创归属

- 原创作者：**Geniucker**。依据本仓库保留的首次提交 `168eab0a54ad167ef04931e5c5e26f604c365be3` 及后续提交作者记录。
- 原项目：[iOSRealRun/iOSRealRun-cli-17](https://github.com/iOSRealRun/iOSRealRun-cli-17)。项目历史相关仓库：[iOSRealRun/iOSRealRun-cli](https://github.com/iOSRealRun/iOSRealRun-cli)。
- 直接克隆来源：[Preisthe/iOSRealRun-cli-17](https://github.com/Preisthe/iOSRealRun-cli-17)，`main` 分支，基线提交 `083f8ec6ddfe558edb48f054222f109673a2f0e6`。
- 保留基线全部 Git 提交历史，包括 Geniucker 和其他贡献者的署名。各贡献者对其贡献的权利不因本仓库发布而转移。
- 本次克隆来源另有 `fix/quic` 分支，本版本未合并该分支，不将该分支的工作归为本次修改。

`run.py` 中坐标转换、路线插值和随机变化，以及 `HNroute.txt` 示例路线等继承自上游。并非此次维护者从零原创。依赖 pymobiledevice3 的设备通信实现由该项目及其贡献者提供。

## 本次适配（2026-10-13）

发布及维护账号：[utenasama](https://github.com/utenasama)。代码适配与文档整理使用 Codex 辅助完成。

- 将 USB 发现、设备检查、PreferredRsdTunnel、DVT 和 LocationSimulation 调用迁移至 pymobiledevice3 11.29.0 的异步接口。
- 加入开发者镜像自动准备、服务检查和单独清除定位模式。
- 用异步等待替换播放忙循环，加入时长、圈数、速度、路线、设备选择及关闭随机变化参数。
- 在正常退出、取消及定位更新失败时尝试清除模拟定位，给连接和清理增加超时。
- 将配置及相对路线路径固定到项目目录；校验路线及速度参数。
- 提供 Miniconda 环境定义、当前与历史依赖清单、自动测试、实机验证记录及中文使用说明。

本次验证设备为 iPhone 16 Pro、iOS 27.0.1。此版本由当前维护者独立发布；问题与兼容性反馈应提交到当前仓库，不应将本次改动视为原作者或上游提供的保证。

## 许可

原项目许可证 MPL-2.0 保留在 [LICENSE](LICENSE)。本次源码修改继续按 MPL-2.0 提供，并依据第 3.3 条处理与 GPL-3.0-or-later 依赖的组合；详见 [LICENSING.md](LICENSING.md)。未删除上游版权、许可或免责声明。
