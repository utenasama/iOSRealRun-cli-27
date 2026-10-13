# 许可与再分发说明

## 本仓库源码

上游项目采用 Mozilla Public License 2.0（MPL-2.0）。[LICENSE](LICENSE) 保留完整原文，原始提交历史和原创归属见 [NOTICE.md](NOTICE.md)。本次新增源码和文档也按 MPL-2.0 提供。使用、修改或分发时请保留适用的版权、许可及免责声明。

本次基线未发现 MPL Exhibit B 所述的 “Incompatible With Secondary Licenses” 标记。代码经修改后仍须按 MPL 提供受保护文件的源码及相应权利，公开仓库提供这些源码和修改记录。

## 与 GPL 依赖组合

运行依赖 **pymobiledevice3 11.29.0** 的发行包元数据声明 `GPL-3.0-or-later`。不能仅凭本仓库的 MPL 文件，推断组合程序只需遵守 MPL。

针对与 pymobiledevice3 组合形成的 Larger Work，本版本依据 **MPL 2.0 第 3.3 条**，将 MPL 受保护源码同时按 MPL-2.0 和 GPL-3.0-or-later 提供；该组合程序按 GPL-3.0-or-later 分发。[COPYING](COPYING) 提供 GPL v3 文本，“or later” 选择依上述许可声明。此安排保留原 MPL 授予的权利，并未将原项目许可证删除或替换。

源码文件中的 MPL 标识应结合本文件阅读：额外的 GPL 分发安排适用于上述组合情形，不能据此将任何无关上游项目任意重新许可。

当前仓库发布的是本项目源码、配置、依赖版本及文档；没有捆绑第三方库源码/二进制、Miniconda 安装器、Apple 开发者镜像或设备配对文件。第三方包由用户从其发行渠道安装。以后如制作包含依赖的可执行文件、镜像或安装包，应提供适用许可证、版权通知及 GPL 所要求的对应源码，不能只附一个许可证名称或上游首页链接。

## 直接依赖

下面依据验证环境的发行包元数据和对应上游项目整理；包自身的许可及版权文件为准。依赖的版权仍归原作者和贡献者所有。

| 包 | 锁定版本 | 声明许可 | 上游源码/署名来源 |
| --- | --- | --- | --- |
| pymobiledevice3 | 11.29.0 | GPL-3.0-or-later | [doronz88/pymobiledevice3](https://github.com/doronz88/pymobiledevice3/tree/v11.29.0)，Doron Ben David 及贡献者 |
| PyYAML | 6.0.1 | MIT | [yaml/pyyaml](https://github.com/yaml/pyyaml/tree/6.0.1)，Kirill Simonov 及贡献者 |
| geopy | 2.4.1 | MIT | [geopy/geopy](https://github.com/geopy/geopy/tree/2.4.1)，项目作者及贡献者 |
| coloredlogs | 15.0.1 | MIT | [xolox/python-coloredlogs](https://github.com/xolox/python-coloredlogs)，Peter Odding 及贡献者 |

完整 Python 包版本清单在 [requirements.lock.txt](requirements.lock.txt)，当前环境依赖许可元数据清单见 [docs/DEPENDENCY-LICENSES.md](docs/DEPENDENCY-LICENSES.md)。间接依赖可能使用不同许可证；元数据空缺不表示没有限制。该清单用于查阅，不替代各包的原始许可，也不覆盖未来版本或旧环境的全部依赖。

## 核对依据

- [MPL 2.0 正文](https://www.mozilla.org/en-US/MPL/2.0/)，特别是 3.1、3.3 和 3.4。
- [Mozilla MPL FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)，Q9 关于修改源码分发，Q14 关于与 GPL 组合。
- [pymobiledevice3 v11.29.0 许可文本](https://github.com/doronz88/pymobiledevice3/blob/v11.29.0/LICENSE) 和安装包的 `License-Expression` 元数据。

以上说明针对当前公开源码及已核对的依赖版本；不同的商业打包、闭源分发或其他使用安排需要按其实际范围重新核对。
