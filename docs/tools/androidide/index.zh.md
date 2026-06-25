---
title: AndroidIDE - 移动应用开发IDE
description: 关于AndroidIDE的全面指南，这是一款可在安卓设备上直接开发安卓应用的开源集成开发环境。
created: 2026-06-25
tags:
  - android-ide
  - mobile-development
  - gradle
  - open-source
  - android-sdk
  - java
  - kotlin
status: draft
---

# AndroidIDE – 在安卓上构建安卓应用

AndroidIDE 是一款**开源的集成开发环境（IDE）**，专为在安卓设备上原生运行而设计。你可以使用 Gradle、智能代码编辑器和终端，在手机或平板上开发完整的安卓应用程序。它是桌面端 Android Studio 工作流的完整替代方案，将整个 Android SDK、构建工具和代码编辑体验带到了移动端。

---

## 什么是 AndroidIDE？

AndroidIDE 将你的安卓设备转变为一个便携式开发工作站。它支持：

- **完整的基于 Gradle 的构建** – 在设备上直接编译、打包和签名 APK 及 Android App Bundle (AAB)。
- **智能代码编辑器** – 为 Java、Kotlin 和 XML 提供语法高亮、自动补全、错误检测和重构功能。
- **集成工具** – Logcat 查看器、Linux 终端（通过 Termux）、文件浏览器、Git 支持和 APK 签名器。
- **项目兼容性** – 导入并处理标准的 Android Studio 项目（Gradle 包装器、build.gradle.kts 等）。

AndroidIDE 采用现代架构，将 IDE 前端与构建/后端进程分离，既强大又针对移动端优化。特别适合学生、爱好者或任何希望在无桌面 PC 的情况下学习或原型开发安卓应用的开发者。

---

## 主要特性

- **完整 Gradle 包装器** – 支持所有标准 Gradle 任务，使用与桌面端相同的 `gradlew` 脚本。
- **多语言代码编辑器** – 支持 Java、Kotlin、XML，提供语义高亮、代码补全和内联错误指示。
- **项目同步** – 自动下载依赖项、SDK 平台和构建工具。
- **APK / AAB 生成** – 调试版和发布版构建，可使用自己的密钥库签名。
- **内置终端** – 真正的 Linux 环境（Termux），可运行自定义命令，如 `adb`、`git` 或 `./gradlew ...`。
- **Logcat 查看器** – 实时查看应用日志输出，进行应用调试。
- **Git 集成** – 在 IDE 内进行基本的版本控制操作（提交、推送、拉取）。
- **文件管理器** – 轻松浏览、重命名、删除项目文件。
- **设备感知** – 自动检测已安装的 JDK、Android SDK、NDK 和 CMake；使用设备 CPU 运行构建。

---

## 为什么选择 AndroidIDE？

- **普及开发** – 任何拥有安卓设备的人都可以开始构建应用，无需拥有 PC。
- **随时调试** – 快速测试和修复问题，无需返回桌面端。
- **教育工具** – 适合在 PC 稀缺的地区教授安卓开发。
- **快速原型** – 构思创意并立即在同一设备上运行。
- **100% 开源** – 基于 GPL-3.0 许可，在 GitHub 上积极维护。

---

## 安装

### 前提条件

- **安卓 7.0（API 24）** 或更高版本
- 至少 **4 GB 内存**（推荐 8 GB）
- 至少 **3 GB 可用存储空间**（如果处理多个项目，则需要更多）
- 相对现代的 SoC（骁龙 8xx、联发科天玑或同等产品）

### 步骤

1. **下载 APK** – 从[官方 GitHub 发布页面](https://github.com/AndroidIDE/AndroidIDE/releases)获取最新版本。  
   （v2.7.1-beta 及更高版本也已在 F-Droid 上提供。）

2. **允许安装未知来源应用** – 在设备设置 → 安全中，为文件管理器或浏览器启用“允许安装未知来源应用”。

3. **安装 APK** – 打开下载的文件并继续安装。

4. **首次启动** – 在提示时授予存储权限。AndroidIDE 将自动下载并设置：
   - OpenJDK 17
   - Android SDK（平台工具、构建工具、最新 SDK 的平台）
   - Gradle 发行版

   根据你的网速和设备性能，初始设置可能需要 **20–30 分钟**。

### 验证安装

设置完成后，你可以在应用内检查已安装的组件：

- **设置 → SDK 管理器** – 显示已安装的 SDK 平台、构建工具和 NDK。
- **终端** – 启动集成终端并运行：
  ```bash
  java -version
  gradle --version
  ```
  以确认 JDK 和 Gradle 已正确配置。

---

## 基本用法

### 创建新项目

1. 打开 AndroidIDE，在欢迎屏幕上点击 **新建项目**。
2. 选择一个模板：**空活动**（Java 或 Kotlin）。
3. 指定：
   - **项目名称**
   - **包名**（例如 `com.example.myapp`）
   - **最低 SDK**（例如 API 24）
   - **语言**（Java 或 Kotlin）
4. 点击 **完成**。IDE 将创建项目（包括 Gradle 包装器、构建脚本和默认源文件）。

### 编写代码

AndroidIDE 的编辑器提供：

- **语法高亮** – 支持 Java、Kotlin、XML 等。
- **自动补全** – 用于类、方法、变量和资源。
- **实时错误检测** – 红色下划线表示编译错误。
- **快速操作** – 导入类、重命名符号、提取方法（重构）。

在项目视图中打开 `MainActivity.java` 或 `MainActivity.kt` 并开始编码。

### 构建和运行

有两种方法可以构建和运行你的应用：

#### 1. 使用 **运行** 按钮（▶️）
- 这会调用 Gradle 的 `assembleDebug` 任务。
- APK 构建完成后，AndroidIDE 会将其直接安装到设备上（无需 ADB 线缆）。
- 如果有模拟器可用（或另一台设备），你可以选择目标。

#### 2. 通过**终端**
打开集成终端（快捷键：`Ctrl+T` 或从菜单中选择）并运行：
```bash
./gradlew assembleDebug
```
生成的 APK 将位于 `app/build/outputs/apk/debug/app-debug.apk`。你可以手动安装：
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```
（ADB 已预配置并可在终端中使用。）

### 使用 Logcat 调试

- 点击 **Logcat** 图标（或选择 **视图 → Logcat**）。
- 按应用的包名过滤。
- 在应用运行时实时查看崩溃堆栈跟踪和调试消息。

### 使用终端

终端是一个完整的 Linux 环境（Termux）。你可以：

- 运行 `./gradlew` 任务，如 `clean`、`test`、`lint`、`assembleRelease`。
- 使用 `git` 命令：`git add .`、`git commit -m "message"`、`git push origin main`。
- 安装额外工具：`pkg install tree` 或 `apt update`。
- 访问 `/storage/emulated/0/` 下的设备存储。

### Git 集成

AndroidIDE 包含一个 **Git 提交** 对话框（从 **VCS** 菜单访问），无需离开 IDE 即可暂存、提交和推送更改。对于更高级的工作流，请使用终端。

---

## 高级用法与命令示例

### Gradle 任务

通过终端运行任何标准 Gradle 任务：

```bash
# 清理构建产物
./gradlew clean

# 构建发布版 APK（未签名）
./gradlew assembleRelease

# 运行 lint 检查
./gradlew lint

# 执行单元测试
./gradlew testDebugUnitTest
```

### 签名发布版 APK

AndroidIDE 提供了一个**密钥库管理器**：

1. 转到 **构建 → 签名与密钥库**。
2. 创建新密钥库或导入现有密钥库。
3. 像在 `app/build.gradle.kts` 中一样配置发布签名：

```kotlin
android {
    ...
    signingConfigs {
        create("release") {
            keyAlias = "releasekey"
            keyPassword = "..."
            storeFile = file("/path/to/keystore.jks")
            storePassword = "..."
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

然后构建：`./gradlew assembleRelease`

签名后的 APK 将生成在 `app/build/outputs/apk/release/` 下。

### 构建 Android App Bundle (AAB)

要生成用于上传 Google Play 的 AAB：

```bash
./gradlew bundleRelease
```

AAB 文件位于 `app/build/outputs/bundle/release/app-release.aab`。

### 自定义构建变体

在 Gradle 脚本中定义风味和构建类型；所有变体均可通过常规 Gradle 命名约定访问：

```bash
./gradlew assembleFlavorDebug
./gradlew assembleFlavorRelease
```

---

## 项目结构及兼容性

AndroidIDE 适用于**标准的 Android Studio 项目**。典型的项目树完全受支持：

```
project/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/...
│   │   │   ├── res/...
│   │   │   └── AndroidManifest.xml
│   │   ├── test/...
│   │   └── androidTest/...
│   ├── build.gradle.kts (或 .groovy)
│   └── proguard-rules.pro
├── gradle/
│   └── wrapper/
├── build.gradle.kts
├── settings.gradle.kts
└── gradlew
```

你可以通过**打开项目**按钮，或将项目文件夹复制到默认工作区（`AndroidIDE/Projects/`）来**导入现有项目**。

> **注意**：建议使用 Gradle 包装器版本 6.0 以上的项目以获得最佳兼容性。基于 NDK/CMake 的项目也可以工作，但在低端硬件上构建时间可能显著增加。

---

## 性能考量

- **构建时间** – 在现代设备（如骁龙 8 Gen 1）上，典型的调试构建需要 2–3 分钟，而开启混淆的发布构建可能需要 5–8 分钟。在较旧的硬件（4GB 内存，Helio G80）上，调试构建预计需要 5–10 分钟。
- **电池与发热** – 编译是 CPU 密集型任务；会明显消耗电池并产生热量。建议使用散热器或确保良好的通风。
- **内存** – 大型项目（超过 1000 个源文件）可能在 4GB 设备上触及内存限制。关闭其他应用会有所帮助。
- **SDK 更新** – AndroidIDE 允许通过 SDK 管理器更新 SDK 组件。但建议不要在移动数据网络下下载大型软件包。

尽管存在这些限制，但换来的是无与伦比的便携性：一个装在口袋里的完整开发环境。

---

## 历史与发展

AndroidIDE 最初由 **terminal_editor** 创建（后由 AndroidIDE 团队维护）。该项目在 **v2.0** 中引起了广泛关注，该版本引入了：

- 完全重写的 IDE 后端。
- 针对移动端优化的 Gradle 包装器。
- 受 Material You 启发的现代 UI。

此后，该项目在 **GitHub** 上**积极维护**（[github.com/AndroidIDE/AndroidIDE](https://github.com/AndroidIDE/AndroidIDE)），定期发布版本、社区翻译和渐进式改进。截至 2026 年 6 月，最新稳定版本为 **v2.7.1-beta**，该版本提供了 F-Droid 支持并进行了各种稳定性修复。

AndroidIDE 由 **Java/Kotlin**（IDE 前端）和 **shell 脚本**（构建编排）组合构建而成。欢迎贡献，该项目拥有活跃的 Discord 社区。

---

## 结论

AndroidIDE 证明了安卓应用开发不再局限于桌面端。凭借其完整的 Gradle 集成、智能代码编辑器和内置调试工具，它是一个强大的环境，适合任何希望仅使用移动设备构建、测试和发布应用的人。虽然它无法与八核桌面 PC 的速度相媲美，但其便利性和开源性质使其成为现代移动优先开发者不可或缺的工具。

**立即开始吧**

- 从 GitHub 下载：[AndroidIDE/releases](https://github.com/AndroidIDE/AndroidIDE/releases)
- 源码与问题跟踪：[AndroidIDE/AndroidIDE](https://github.com/AndroidIDE/AndroidIDE)
- F-Droid（v2.7.1+）：在 F-Droid 商店中搜索 “AndroidIDE”。