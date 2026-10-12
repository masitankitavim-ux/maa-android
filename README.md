# MAA Android

把 [MaaAssistantArknights](https://github.com/MaaAssistantArknights/MaaAssistantArknights)（MAA）的 arm64 Android 内核做成 **Magisk 模块**，并附带一个**手机端 Web 控制台**，功能对齐 MAA 电脑端。

- 模块开机后自动拉起控制台，无需手动敲命令。
- 自动从 MAA 官方 Release 下载 / 更新 arm64 内核与资源（`maactl ensure|update`）。
- 控制台是单页 Web UI，浏览器访问 `http://<手机IP>:8790` 即可操作。
- 内置明日方舟主题桌宠（维维美 Vivimi，Petdex sprite 动画）。

## 组成

| 目录 | 内容 |
|------|------|
| `maaweb/` | Go 写的 Web 控制台（HTTP 服务 + MAA 内核绑定 + 静态 UI） |
| `maaweb/webui/` | 前端单页 `index.html` 与桌宠 sprite `vivimi.webp` |
| `nativeext/` | `libMaaNativeExt.so` 的 C 源码（Android 原生触控 / 截图注入） |
| `module/` | Magisk 模块骨架：`module.prop`、`customize.sh`、`service.sh`、`maactl`、`META-INF/` |
| `scripts/` | 交叉编译与打包脚本 |

## 控制台功能

- **连接设置**：客户端类型、游戏包名、ADB 地址/端口、触控模式、分辨率、显示 ID。
- **一键长草**：StartUp / Fight / Recruit / Infrast / Mall / Award / Roguelike / Copilot / Depot / OperBox / CloseDown 全部子任务参数，中文说明，逐项可配。
- **运行控制**：开始 / 停止 / 返回主界面 / 手动截图 / 点击。
- **定时任务**：每天定点自动启动游戏并执行一键长草，可开关、可设时间、可选任务清单。
- **状态与日志**：实时状态、精简运行日志、截图预览（可滚动）。
- **自动更新**：一键检查并更新 MAA 内核组件。
- **主题与桌宠**：明日方舟主题，维维美 sprite 桌宠（拖拽 / 说话 / 随机漫步）。

## 环境要求

- arm64（aarch64）Android 设备
- Magisk / KernelSU（支持 `/data/adb/modules` 与 `service.sh`）
- 设备已 root

## 构建

### 1. 交叉编译控制台（Windows + Android NDK）

```sh
# 依赖：Go 1.22+、Android NDK r26/r27
export GOOS=android GOARCH=arm64 CGO_ENABLED=1
export CC=$NDK/toolchains/llvm/prebuilt/windows-x86_64/bin/aarch64-linux-android21-clang.cmd
export CGO_CFLAGS='--target=aarch64-linux-android21 -O2'
export CGO_LDFLAGS='--target=aarch64-linux-android21'
cd maaweb && go build -trimpath -ldflags '-s -w' -o maaweb .
```

见 `scripts/build-maaweb.sh`。

### 2. 打包 Magisk 模块

```sh
# 把编译好的 maaweb 与 libMaaNativeExt.so 放进 module/ 后打包
bash scripts/pack-module.sh
```

产物为 `maa_android-<version>.zip`，用 Magisk 刷入。

## 内核组件来源

MAA 内核（`libMaaCore.so` 等）与资源不随仓库分发，首次开机由 `maactl ensure` 从官方 Release 下载：

- 版本查询：`https://api.github.com/repos/MaaAssistantArknights/MaaAssistantArknights/releases/latest`
- 组件包：`MAAComponent-<tag>-android-arm64.tar.gz`
- 下载走 `gh-proxy.com` 镜像，便于国内直连。

## 设备端目录

| 路径 | 说明 |
|------|------|
| `/data/adb/maa/lib` | MAA 内核 `.so` 与 `libMaaNativeExt.so` |
| `/data/adb/maa/resource` | MAA 资源（`config.json` 等） |
| `/data/adb/maa/ocr-ncnn` | 自带的 ncnn OCR 模型（覆盖官方包内模型） |
| `/data/adb/maa/maaweb.log` | 控制台日志 |

## 许可

MIT。MAA 内核与资源版权归 MaaAssistantArknights 项目所有，本项目仅做封装与移动端控制台。

桌宠素材来自 [Petdex](https://petdex.dev/) 的 Vivimi（Arknights W / 维维美皮肤）动画雪碧图，仅供个人使用。
