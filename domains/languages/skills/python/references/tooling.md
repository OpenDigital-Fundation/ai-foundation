# Python — Tooling

Part of `languages:python`. Load when formatters, linters, type checkers and editor hooks.

## Python Hooks

<!-- source: affaan-m/ECC rules/python/hooks.md -->

> This file extends common/hooks.md with Python specific content.

### PostToolUse Hooks

Configure in `~/.claude/settings.json`:

- **black/ruff**: Auto-format `.py` files after edit
- **mypy/pyright**: Run type checking after editing `.py` files

### Warnings

- Warn about `print()` statements in edited files (use `logging` module instead)

## Generating Python Installer (Commercial-Grade)

<!-- source: affaan-m/ECC skills/generating-python-installer/SKILL.md -->

You are a **Python commercial deployment expert**. Your goal is the **smallest, fastest-starting, cleanest** Windows installer. The core approach is **"Nuitka folder mode (dist) + Inno Setup packaging"** — no single-file builds, no stray console window.

### When to Activate

Activate when the user explicitly asks for **advanced** Python packaging or size/startup optimization on Windows:

- Nuitka extreme / commercial-grade compilation, smallest-size or fastest-startup builds
- `dist` folder slimming, DLL footprint analysis, 32-bit vs 64-bit size tradeoffs
- Inno Setup packaging with full metadata and a clean, residue-free uninstall

This skill targets advanced size/startup optimization — not basic one-file "script to exe" conversion.

### How It Works

1. **Confirm build parameters** — app name, version, publisher, exe name, source/output dirs, icon. Never auto-fill; ask the user.
2. **Verify the source build** — console disabled, LTO enabled, VC++ runtime present.
3. **Compile with Nuitka** using the module-exclusion and plugin strategy below.
4. **Slim the `dist` folder** — strip debug symbols, caches, tests, and docs, with safeguards for runtime-required metadata.
5. **Analyze DLLs** to find and trim the largest dependencies.
6. **Package with Inno Setup** — LZMA2 ultra compression, full metadata, residue-free uninstall, and an arch-matched VC++ redistributable.

### Examples

- "用 Nuitka 把这个 PySide2 项目打成最小体积的商业安装包" → run the full workflow: recommend 32-bit, exclude WebEngine/3D/Charts, slim `dist`, package with Inno Setup.
- "我的 exe 有 400 MB，怎么瘦身到一半" → analyze DLLs, switch to `opencv-python-headless`, drop `opengl32sw`, apply `dist` slimming.
- "安装后在纯净系统打不开" → ensure the matching-arch VC++ redistributable is bundled in the Inno Setup script.

---

### 核心理念

坚持 **"Nuitka 文件夹模式(dist) + Inno Setup 封装"** 方案。拒绝单文件版，拒绝黑窗。

---

### 实战参考案例（生产级 PySide2 桌面应用，323 MB，含 OpenCV / Playwright）

#### 项目概况
- **总体积**: 323 MB
- **打包工具**: PyInstaller 4.7 (32位)
- **主要依赖**: PySide2 (22.52 MB), OpenCV (62.38 MB), Playwright (76.74 MB)
- **Python 版本**: Python 3.8 (32位)
- **DLL 数量**: 71 个，总计 93.23 MB

#### 关键优化策略
1. PASS: **使用 32 位 Python** → 体积减少 20-30%
2. PASS: **base_library.zip 压缩标准库** → 0.74 MB
3. PASS: **精简模块排除** → 无 pytest/unittest/setuptools
4. PASS: **精简 Qt 插件** → 只保留必要插件

#### 体积分布

| 组件 | 体积 | 占比 | 优化建议 |
|------|------|------|---------|
| playwright | 76.74 MB | 23.8% | 非必要可移除 |
| OpenCV | 62.38 MB | 19.3% | 用 opencv-python-headless |
| PySide2 | 22.52 MB | 7.0% | 排除 WebEngine/3D/Charts |
| 其他依赖 | 161.36 MB | 49.9% | - |

#### 预期效果对比

| 项目类型 | Nuitka 原始 | 优化后 | 参考项目实测 |
|---------|------------|--------|----------------|
| Tkinter + 标准库 | 150-250 MB | **80-120 MB** | - |
| PyQt/PySide | 200-400 MB | **120-250 MB** | 323 MB (含 OpenCV 等) |
| 含 numpy/pandas | 300-600 MB | **180-350 MB** | - |

---

### 核心工作流 (Workflow) - WARNING: 严格执行

当用户请求打包时，按照以下步骤操作：

**步骤 1：强制参数确认（FAIL: 禁止使用默认值）**

> **WARNING: 重要规则：以下所有参数必须逐一向用户确认，禁止自动填充或使用默认值！**

必须向用户询问并确认以下信息（*等待用户明确回复后才能继续*）：

| 参数 | 说明 | 示例 |
|------|------|------|
| **软件名称** (App Name) | 软件显示名称 | `红墨批注` |
| **版本号** (Version) | 语义化版本号 | `1.0.0` |
| **发布者/公司名** (Publisher) | 控制面板显示的发布者 | `YourCompany` |
| **主程序** (Exe Name) | 主可执行文件名 | `RedInk.exe` |
| **源路径** (Source Dir) | Nuitka dist 文件夹绝对路径 | `D:\project\dist` |
| **输出路径** (Output Dir) | 安装包生成位置 | `D:\project\output` |
| **图标路径** (Icon Path) | .ico 文件绝对路径（可选但推荐） | `D:\project\icon.ico` |
| **官网地址** (URL) | 可选，用于控制面板链接 | `https://example.com` |

**询问模板：**
> "请提供以下打包参数，我需要您逐一确认：
> 1. 软件名称：
> 2. 版本号：
> 3. 发布者/公司名：
> 4. 主程序文件名（如 xxx.exe）：
> 5. 源路径（Nuitka dist 文件夹）：
> 6. 输出路径（安装包保存位置）：
> 7. 图标路径（.ico 文件，可留空）：
> 8. 官网地址（可留空）：
>
> 请逐一填写，或回复"跳过"表示使用空值。"

**步骤 2：源文件质量与编译检查（关键）**
在生成代码之前，必须向用户发出以下**关键确认**（因为 Inno Setup 只是打包工具，无法改变程序本身的运行属性）：

> "WARNING: **编译参数检查**：
> 1. **去黑窗**：请确认您的 dist 文件夹是使用 `nuitka --windows-console-mode=disable` 编译的。（否则安装后依然会有黑框）
> 2. **高性能**：请确认是否使用了 `--lto=yes`。（否则启动速度可能不理想）
> 3. **运行库**：请确保 dist 文件夹内已包含必要的 VC++ 运行库，防止在纯净系统上无法运行。
>
> **确认源文件已准备好请回复"确认"，否则请先重新编译。**"

**步骤 3：生成代码**
用户确认后，输出包含 **完整元数据** 和 **卸载图标修复** 的代码。

---

### Nuitka 极限优化编译（基于 参考项目经验）

#### 一、32 位 vs 64 位选择策略

**参考项目使用 32 位 Python 的原因**：

| 组件 | 64位体积 | 32位体积 | 节省 |
|------|---------|---------|------|
| python3x.dll | ~4.5 MB | ~3.8 MB | 15% |
| Qt5Core.dll | ~8 MB | ~5 MB | 37% |
| numpy | ~30 MB | ~20 MB | 33% |
| **总体** | 基准 | **-20~30%** | - |

**推荐使用 32 位条件**：
- PASS: 程序内存占用 < 2GB
- PASS: 不处理超大文件（< 2GB）
- PASS: 目标用户是普通办公电脑

**32 位编译方法**：
```bash
# 1. 安装 32 位 Python（和 64 位可以共存）
# 下载地址：https://www.python.org/downloads/windows/

# 2. 用 32 位 Python 安装依赖
py -3.12-32 -m pip install -r requirements.txt

# 3. 用 32 位 Python 编译
py -3.12-32 -m nuitka --standalone ...你的参数
```

#### 二、模块排除清单（参考项目验证过的）

**安全排除列表**（运行时不需要）：
```
unittest,test,pytest,_pytest,doctest,pdb,pdbpp,
setuptools,pip,distutils,pkg_resources,
email.mime,http.server,xmlrpc,pydoc
```

**预期效果**：节省 **30-50 MB**

#### 三、GUI 框架专用优化

##### Tkinter 极限优化（推荐，最轻量）
```bash
nuitka --standalone --windows-console-mode=disable ^
    --lto=yes ^
    --jobs=8 ^
    --enable-plugin=tk-inter ^
    --enable-plugin=anti-bloat ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    --nofollow-import-to=unittest,test,pytest,_pytest,doctest,pdb,pdbpp ^
    --nofollow-import-to=setuptools,pip,distutils,pkg_resources ^
    --nofollow-import-to=email.mime,http.server,xmlrpc,pydoc ^
    --python-flag=no_docstrings ^
    --output-dir=dist ^
    --windows-icon-from-ico=icon.ico ^
    --remove-output ^
    main.py
```

**预期体积**：80-120 MB（优化后）

##### PyQt5 / PySide2 优化
```bash
nuitka --standalone --windows-console-mode=disable ^
    --lto=yes ^
    --jobs=8 ^
    --enable-plugin=pyqt5 ^
    --enable-plugin=anti-bloat ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    --nofollow-import-to=unittest,test,pytest,_pytest,doctest,pdb ^
    --nofollow-import-to=setuptools,pip,distutils,pkg_resources ^
    --nofollow-import-to=PyQt5.QtWebEngine,PyQt5.QtWebEngineWidgets ^
    --nofollow-import-to=PyQt5.Qt3D,PyQt5.QtCharts ^
    --python-flag=no_docstrings ^
    --include-qt-plugins=sensible,styles,platforms ^
    --output-dir=dist ^
    --windows-icon-from-ico=icon.ico ^
    --remove-output ^
    main.py
```

**预期体积**：120-250 MB（优化后）

#### 四、一键编译脚本模板

**保存为 `build_optimized.bat`（项目根目录）**：

```batch
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo Nuitka 极限优化编译（参考 参考项目）
echo ========================================

REM === 配置区域（请修改为你的实际值） ===
set APP_NAME=你的软件名
set MAIN_FILE=main.py
set ICON_FILE=icon.ico

REM === 自动检测 CPU 核心数 ===
REM 用 Windows 自带环境变量（wmic 在 Win11 22H2+ 已移除，探不到会让 --jobs=0 单线程编译）
set CPU_CORES=%NUMBER_OF_PROCESSORS%
if not defined CPU_CORES set CPU_CORES=4
set /a BUILD_JOBS=%CPU_CORES%

REM === 参考项目的模块排除清单 ===
set EXCLUDE_MODULES=unittest,test,pytest,_pytest,doctest,pdb,pdbpp
set EXCLUDE_MODULES=%EXCLUDE_MODULES%,setuptools,pip,distutils,pkg_resources
set EXCLUDE_MODULES=%EXCLUDE_MODULES%,email.mime,http.server,xmlrpc,pydoc

echo.
echo [1/4] 清理旧编译...
if exist dist rd /s /q dist
if exist build rd /s /q build

echo.
echo [2/4] Nuitka 编译中（应用 参考项目优化策略）...
echo - CPU 核心: %CPU_CORES% (使用 %BUILD_JOBS% 线程)
echo - 模块排除: %EXCLUDE_MODULES%
echo.

nuitka --standalone ^
    --windows-console-mode=disable ^
    --lto=yes ^
    --jobs=%BUILD_JOBS% ^
    --enable-plugin=anti-bloat ^
    --enable-plugin=tk-inter ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    --nofollow-import-to=%EXCLUDE_MODULES% ^
    --python-flag=no_docstrings ^
    --output-dir=dist ^
    --windows-icon-from-ico=%ICON_FILE% ^
    --remove-output ^
    %MAIN_FILE%

if %errorlevel% neq 0 (
    echo.
    echo [错误] 编译失败！
    pause
    exit /b 1
)

echo.
echo [3/4] 统计编译结果...
for /f %%a in ('powershell -NoProfile -Command "(Get-ChildItem -LiteralPath 'dist\%APP_NAME%.dist' -Recurse -File | Measure-Object -Property Length -Sum).Sum"') do set TOTAL_SIZE=%%a
set TOTAL_SIZE=%TOTAL_SIZE:,=%
set /a SIZE_MB=%TOTAL_SIZE% / 1048576
echo - 编译后体积: %SIZE_MB% MB

echo.
echo [4/4] 执行瘦身清理（参考 参考项目策略）...
powershell -ExecutionPolicy Bypass -File slim_dist.ps1 -DistPath "dist\%APP_NAME%.dist"

echo.
echo ========================================
echo 编译完成！
echo ========================================
pause
```

#### 五、dist 瘦身脚本（参考项目级别清理）

**保存为 `slim_dist.ps1`（和 build_optimized.bat 同目录）**：

```powershell
param(
    [string]$DistPath
)

$ErrorActionPreference = "Continue"  # 不静默吞错：删除失败会显示出来，避免假成功

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "dist 瘦身清理（参考 参考项目策略）" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (-not (Test-Path $DistPath)) {
    Write-Host "[错误] 找不到目录: $DistPath" -ForegroundColor Red
    exit 1
}

# 统计初始体积
$InitialSize = (Get-ChildItem -Path $DistPath -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "`n初始体积: $([math]::Round($InitialSize, 2)) MB" -ForegroundColor Yellow

# 参考项目特征：没有 .pdb, .pyi, __pycache__, test 等
Write-Host "`n[应用 参考项目的清理策略...]" -ForegroundColor Green

# 1. 删除调试符号
Write-Host "`n[1/7] 删除 .pdb 调试符号..." -ForegroundColor Green
$pdbFiles = Get-ChildItem -Path $DistPath -Recurse -Include *.pdb -File
$pdbSize = ($pdbFiles | Measure-Object -Property Length -Sum).Sum / 1MB
if ($pdbFiles.Count -gt 0) {
    $pdbFiles | Remove-Item -Force
    Write-Host "  删除 $($pdbFiles.Count) 个文件，节省 $([math]::Round($pdbSize, 2)) MB"
} else {
    Write-Host "  未发现 .pdb 文件（已优化）" -ForegroundColor Gray
}

# 2. 删除类型提示
Write-Host "`n[2/7] 删除 .pyi 类型提示..." -ForegroundColor Green
$pyiFiles = Get-ChildItem -Path $DistPath -Recurse -Include *.pyi -File
$pyiSize = ($pyiFiles | Measure-Object -Property Length -Sum).Sum / 1MB
if ($pyiFiles.Count -gt 0) {
    $pyiFiles | Remove-Item -Force
    Write-Host "  删除 $($pyiFiles.Count) 个文件，节省 $([math]::Round($pyiSize, 2)) MB"
} else {
    Write-Host "  未发现 .pyi 文件（已优化）" -ForegroundColor Gray
}

# 3. 删除 __pycache__
Write-Host "`n[3/7] 删除 __pycache__ 缓存..." -ForegroundColor Green
$pycacheDirs = Get-ChildItem -Path $DistPath -Recurse -Directory -Filter "__pycache__"
$pycacheSize = 0
foreach ($dir in $pycacheDirs) {
    $size = (Get-ChildItem -Path $dir.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $pycacheSize += $size
    Remove-Item -Path $dir.FullName -Recurse -Force
}
if ($pycacheDirs.Count -gt 0) {
    Write-Host "  删除 $($pycacheDirs.Count) 个目录，节省 $([math]::Round($pycacheSize / 1MB, 2)) MB"
} else {
    Write-Host "  未发现 __pycache__（已优化）" -ForegroundColor Gray
}

# 4. 删除测试目录
Write-Host "`n[4/7] 删除 test/tests 测试目录..." -ForegroundColor Green
$testDirs = Get-ChildItem -Path $DistPath -Recurse -Directory | Where-Object { $_.Name -match '^tests?$' }
$testSize = 0
foreach ($dir in $testDirs) {
    $size = (Get-ChildItem -Path $dir.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $testSize += $size
    Remove-Item -Path $dir.FullName -Recurse -Force
}
if ($testDirs.Count -gt 0) {
    Write-Host "  删除 $($testDirs.Count) 个目录，节省 $([math]::Round($testSize / 1MB, 2)) MB"
} else {
    Write-Host "  未发现测试目录（已优化）" -ForegroundColor Gray
}

# 5. 删除文档和示例
Write-Host "`n[5/7] 删除 docs/examples 文档目录..." -ForegroundColor Green
$docDirs = Get-ChildItem -Path $DistPath -Recurse -Directory | Where-Object { $_.Name -match '^(docs|examples|samples|demo)$' }
$docSize = 0
foreach ($dir in $docDirs) {
    $size = (Get-ChildItem -Path $dir.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $docSize += $size
    Remove-Item -Path $dir.FullName -Recurse -Force
}
if ($docDirs.Count -gt 0) {
    Write-Host "  删除 $($docDirs.Count) 个目录，节省 $([math]::Round($docSize / 1MB, 2)) MB"
} else {
    Write-Host "  未发现文档目录（已优化）" -ForegroundColor Gray
}

# 6. 删除 .pyc 文件
Write-Host "`n[6/7] 删除 .pyc 字节码..." -ForegroundColor Green
$pycFiles = Get-ChildItem -Path $DistPath -Recurse -Include *.pyc -File
$pycSize = ($pycFiles | Measure-Object -Property Length -Sum).Sum / 1MB
if ($pycFiles.Count -gt 0) {
    $pycFiles | Remove-Item -Force
    Write-Host "  删除 $($pycFiles.Count) 个文件，节省 $([math]::Round($pycSize, 2)) MB"
} else {
    Write-Host "  未发现 .pyc 文件（已优化）" -ForegroundColor Gray
}

# 7. 精简 .dist-info 元数据
Write-Host "`n[7/7] 精简 .dist-info 元数据..." -ForegroundColor Green
$distInfoDirs = Get-ChildItem -Path $DistPath -Recurse -Directory -Filter "*.dist-info"
$removedCount = 0
$removedSize = 0
foreach ($infoDir in $distInfoDirs) {
    # 仅删安装期记账文件；保留 METADATA 与 entry_points.txt（运行期被 importlib.metadata 读取，删除会破坏插件发现）
    $filesToRemove = @("RECORD", "INSTALLER", "direct_url.json")
    foreach ($fileName in $filesToRemove) {
        $file = Join-Path $infoDir.FullName $fileName
        if (Test-Path $file) {
            $size = (Get-Item $file).Length
            $removedSize += $size
            Remove-Item $file -Force
            $removedCount++
        }
    }
}
if ($removedCount -gt 0) {
    Write-Host "  删除 $removedCount 个元数据文件，节省 $([math]::Round($removedSize / 1MB, 2)) MB"
} else {
    Write-Host "  未发现可清理的元数据（已优化）" -ForegroundColor Gray
}

# 统计最终体积
$FinalSize = (Get-ChildItem -Path $DistPath -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
$SavedSize = $InitialSize - $FinalSize
$SavedPercent = if ($InitialSize -gt 0) { ($SavedSize / $InitialSize) * 100 } else { 0 }

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "清理完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "初始体积: $([math]::Round($InitialSize, 2)) MB" -ForegroundColor Yellow
Write-Host "最终体积: $([math]::Round($FinalSize, 2)) MB" -ForegroundColor Green
Write-Host "节省空间: $([math]::Round($SavedSize, 2)) MB ($([math]::Round($SavedPercent, 1))%)" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 对比 参考项目
Write-Host "[对比参考]" -ForegroundColor Yellow
Write-Host "参考项目总体积: 323 MB (包含 PyQt, OpenCV, Playwright 等重量级库)" -ForegroundColor Gray
Write-Host "如果你的项目是纯 Tkinter + 标准库，目标应该在 80-150 MB" -ForegroundColor Gray
```

**预期效果**：节省 **15-30%** 体积

#### 六、DLL 依赖分析工具

**保存为 `analyze_dlls.py`（用于找出体积大户）**：

```python
"""
DLL 依赖分析工具
参考 参考项目的 DLL 管理策略，帮助识别体积大户和优化建议
"""
import sys
from pathlib import Path

def analyze_dlls(dist_path: str):
    """分析 dist 目录中的 DLL 依赖"""
    dist_dir = Path(dist_path)

    if not dist_dir.exists():
        print(f"[错误] 目录不存在: {dist_path}")
        return

    print("=" * 70)
    print("DLL 依赖分析（参考 参考项目策略）")
    print("=" * 70)

    # 收集所有 DLL
    dll_files = list(dist_dir.rglob("*.dll"))

    if not dll_files:
        print("\n未发现 DLL 文件")
        return

    # 按大小排序
    dll_data = [(dll, dll.stat().st_size) for dll in dll_files]
    dll_data.sort(key=lambda x: x[1], reverse=True)

    total_size = sum(size for _, size in dll_data)

    print(f"\n总 DLL 数量: {len(dll_files)}")
    print(f"总 DLL 体积: {total_size / 1024 / 1024:.2f} MB\n")

    # 参考项目对比
    print("[对比参考] 参考项目的 DLL 情况:")
    print("  - 总数量: 71 个")
    print("  - 总体积: 93.23 MB")
    print("  - 最大的: libopenblas (26.85 MB), opengl32sw (15.25 MB)\n")

    # 分析大于 3MB 的 DLL
    large_dlls = [(dll, size) for dll, size in dll_data if size > 3 * 1024 * 1024]

    if large_dlls:
        print("=" * 70)
        print("WARNING:  大于 3MB 的 DLL（需重点关注）")
        print("=" * 70)

        for dll, size in large_dlls:
            size_mb = size / 1024 / 1024
            relative_path = dll.relative_to(dist_dir)
            name_lower = dll.name.lower()

            print(f"\n{size_mb:8.2f} MB  {dll.name}")
            print(f"           位置: {relative_path.parent}")

            # 优化建议
            suggestions = get_optimization_suggestion(name_lower)
            if suggestions:
                for suggestion in suggestions:
                    print(f"            {suggestion}")

    # 检查冗余 DLL
    print("\n" + "=" * 70)
    print(" 冗余检查")
    print("=" * 70)

    # 检查调试版本
    debug_dlls = [dll for dll, _ in dll_data if dll.stem.endswith('d')]
    if debug_dlls:
        print(f"\nWARNING:  发现 {len(debug_dlls)} 个调试版本 DLL（可以删除）:")
        for dll in debug_dlls:
            print(f"  - {dll.name}")
    else:
        print("\nPASS: 未发现调试版本 DLL（已优化）")

    # VC++ Runtime
    vc_runtimes = [dll for dll, _ in dll_data if 'vcruntime' in dll.name.lower() or 'msvcp' in dll.name.lower()]
    if vc_runtimes:
        print(f"\n[VC++ Runtime 库] 发现 {len(vc_runtimes)} 个:")
        for dll in vc_runtimes:
            size_mb = dll.stat().st_size / 1024 / 1024
            print(f"  - {dll.name} ({size_mb:.2f} MB)")
        print("   这些是必需的，参考项目也包含了这些文件")

    # 全部 DLL 列表
    print("\n" + "=" * 70)
    print(" 完整 DLL 列表（按体积排序，前 20）")
    print("=" * 70)
    print(f"\n{'体积 (MB)':>10}  {'文件名':<30}  位置")
    print("-" * 70)

    for dll, size in dll_data[:20]:
        size_mb = size / 1024 / 1024
        relative_path = dll.relative_to(dist_dir)
        location = str(relative_path.parent) if relative_path.parent != Path('.') else "根目录"
        print(f"{size_mb:10.2f}  {dll.name:<30}  {location}")

    if len(dll_data) > 20:
        remaining_size = sum(size for _, size in dll_data[20:]) / 1024 / 1024
        print(f"... 还有 {len(dll_data) - 20} 个 DLL，共 {remaining_size:.2f} MB")


def get_optimization_suggestion(dll_name: str) -> list:
    """根据 DLL 名称给出优化建议"""
    suggestions = []

    if "openblas" in dll_name or "mkl" in dll_name:
        suggestions.append("数学运算库，参考项目的 libopenblas 有 26.85 MB")
        suggestions.append("如不需要高性能计算可考虑轻量版")

    elif "opencv" in dll_name or "ffmpeg" in dll_name:
        suggestions.append("OpenCV 相关，参考项目的 opencv_videoio_ffmpeg 有 18.48 MB")
        suggestions.append("考虑用 opencv-python-headless")

    elif "qt5" in dll_name or "qt6" in dll_name or "pyside" in dll_name:
        suggestions.append("Qt 库，参考项目的 Qt5Core 有 5.13 MB")
        suggestions.append("可排除不需要的模块（WebEngine, 3D, Charts）")

    elif "opengl" in dll_name and "sw" in dll_name:
        suggestions.append("OpenGL 软件渲染器，参考项目保留了 15.25 MB")
        suggestions.append("通常可以删除（使用硬件渲染）")

    elif "d3dcompiler" in dll_name:
        suggestions.append("DirectX 编译器，参考项目有 3.53 MB")

    elif "mfc140" in dll_name:
        suggestions.append("MFC 库，参考项目有 4.89 MB")

    return suggestions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_dlls.py <dist目录路径>")
        print("示例: python analyze_dlls.py dist/main.dist")
        sys.exit(1)

    analyze_dlls(sys.argv[1])
```

**使用方法**：
```bash
python analyze_dlls.py dist/你的软件名.dist
```

---

### 完整优化工作流

#### 步骤 1：修改编译脚本配置

编辑 `build_optimized.bat`，修改这 3 行：

```batch
set APP_NAME=你的软件名      REM 改成实际名称
set MAIN_FILE=main.py        REM 你的主程序文件
set ICON_FILE=icon.ico       REM 你的图标文件
```

#### 步骤 2：一键编译+瘦身

```bash
# 在项目根目录执行
build_optimized.bat
```

#### 步骤 3：分析 DLL 依赖

```bash
python analyze_dlls.py dist/你的软件名.dist
```

#### 步骤 4：根据分析结果优化

**如果用了 OpenCV** → 改用无头版
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

**如果用了 Qt** → 排除不需要的模块
```batch
# 在编译命令中添加
--nofollow-import-to=PyQt5.QtWebEngine,PyQt5.Qt3D,PyQt5.QtCharts
```

**删除软件渲染器**（如果不需要）
```powershell
# 在 dist 目录执行
Remove-Item "opengl32sw.dll" -Force
```

---

### VC++ 运行库处理方案

#### 方案一：静态链接（推荐）
```bash
nuitka --static-libpython=yes ...
```

#### 方案二：捆绑运行库安装（商业发布推荐）
在 Inno Setup 脚本中添加：

```iss
; WARNING: VC++ 运行库架构必须与 Python/Nuitka 构建架构一致。
; 本 skill 推荐 32 位 Python，故默认捆绑 vc_redist.x86.exe；
; 若用 64 位 Python 编译，请把下面两处改为 vc_redist.x64.exe。
[Files]
Source: "{#MySourceDir}\..\vc_redist.x86.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "{tmp}\vc_redist.x86.exe"; Parameters: "/quiet /norestart"; StatusMsg: "正在安装运行库..."; Flags: waituntilterminated
```

> 下载地址：[Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

---

### Inno Setup 脚本模板（商业终极版）

```iss
; =====================================================================
;  WARNING: 商业级 Python 安装脚本 (Inno Setup 6.x)
;  特性：LZMA2 极限压缩 | 全中文 | 完整元数据 | 无残留卸载
;  参考：参考项目(323 MB, LZMA2 压缩)
; =====================================================================

; --- 1. 参数定义 ---
#define MyAppName        "{{APP_NAME}}"
#define MyAppVersion     "{{APP_VERSION}}"
#define MyAppPublisher   "{{PUBLISHER}}"
#define MyAppURL         "{{APP_URL}}"
#define MyAppExeName     "{{EXE_NAME}}"
#define MySourceDir      "{{SOURCE_DIR}}"
#define MyOutputDir      "{{OUTPUT_DIR}}"
;#define MyIconPath      "{{ICON_PATH}}"

[Setup]
; --- 身份识别 ---
AppId={{GENERATE_RANDOM_GUID}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; --- 安装路径与权限 ---
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableDirPage=no
DisableProgramGroupPage=no
PrivilegesRequired=admin

; --- 输出设置 ---
OutputDir={#MyOutputDir}
OutputBaseFilename=Setup_{#MyAppName}_v{#MyAppVersion}

; --- 视觉体验 ---
WizardStyle=modern
#ifdef MyIconPath
SetupIconFile={#MyIconPath}
UninstallDisplayIcon={app}\{#MyAppExeName}
#endif

; ---  核心压缩 (参考 参考项目) ---
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; --- 架构 ---
; 注意：仅 64 位 Python 构建才设此项。本 skill 推荐 32 位 Python——
; 32 位构建请保持注释，使应用按 32 位安装并与上面捆绑的 vc_redist.x86.exe 匹配。
; 仅当用 64 位 Python 编译时才取消注释。
;ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[UninstallDelete]
Type: filesandordirs; Name: "{app}\*"

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
```

---

### 占位符说明

| 占位符 | 说明 | 示例值 |
|--------|------|--------|
| `{{APP_NAME}}` | 软件显示名称 | `红墨批注` |
| `{{APP_VERSION}}` | 版本号 | `1.0.0` |
| `{{PUBLISHER}}` | 发布者/公司名 | `MyCompany` |
| `{{APP_URL}}` | 官网地址 | `https://example.com` |
| `{{EXE_NAME}}` | 主程序文件名 | `RedInk.exe` |
| `{{SOURCE_DIR}}` | Nuitka dist 文件夹路径 | `D:\project\dist\RedInk.dist` |
| `{{OUTPUT_DIR}}` | 安装包输出路径 | `D:\project\output` |
| `{{ICON_PATH}}` | 图标文件路径 | `D:\project\icon.ico` |
| `{{GENERATE_RANDOM_GUID}}` | **需生成唯一GUID** | 使用 Inno Setup "Tools > Generate GUID" |

---

### 常见问题 (FAQ)

#### Q1: 安装后双击程序无反应？
1. 打开 CMD，手动运行 exe 查看错误信息
2. 检查是否缺少 VC++ 运行库
3. 检查 Nuitka 编译是否成功

#### Q2: 安装包体积过大？
**优化方法**：
1. 使用 32 位 Python 编译（节省 20-30%）
2. 应用 参考项目的模块排除清单
3. 启用 Anti-Bloat 插件
4. 执行 dist 文件夹瘦身脚本
5. 分析 DLL，移除不必要的大文件

#### Q3: 杀毒软件误报？
**解决方案**：
- 提交到主流杀毒厂商进行白名单申请
- 购买代码签名证书（推荐：Sectigo, DigiCert）
- 避免使用 UPX 压缩

#### Q4: 安装时提示 Windows 已保护你的电脑？
- 购买 EV 代码签名证书（可立即获得信任）
- 普通代码签名证书需要积累安装量后逐渐获得信任

---

### 实战问题处理记录（更新 2026-02-07）

- **安装后提示缺少 python3xx.dll**：必须使用 Nuitka `--standalone`；确认 dist 内存在该 dll；不要打单文件版。
- **安装后点击无反应**：GUI 启动期可能被重依赖阻塞；将重依赖延迟到"开始导出"再 import；添加日志排查。
- **Nuitka + MinGW 在非 ASCII 路径报错**：把源码复制到 ASCII 目录再编译；设置 `PYTHONIOENCODING=utf-8`。
- **Inno Setup 警告 `x64` 已弃用（仅 64 位构建需要 64 位安装模式时）**：改为 `ArchitecturesInstallIn64BitMode=x64compatible`；32 位构建无需此项。
- **`--disable-console` 已废弃**：改用 `--windows-console-mode=disable`。
- **dist 出现 `_nuitka_temp.exe`**：在 [Files] 中排除它。

---

### 优化效果预期

| 优化组合 | 体积减少 | 启动提升 | 风险等级 |
|----------|----------|----------|----------|
| 基础编译 | 基准 | 基准 | 无 |
| + `--lto=yes` | 5-10% | 10-20% | PASS: 无 |
| + anti-bloat | 15-25% | - | PASS: 无 |
| + 模块排除 | 20-35% | 5% | PASS: 无 |
| + dist 瘦身 | 25-40% | - | PASS: 无 |
| + 32 位编译 | 40-60% | - | PASS: 无 |
| **全部组合** | **45-65%** | **15-25%** | PASS: **无风险** |

> WARNING: **不建议使用 UPX 压缩**，虽然能进一步减小体积，但极易触发杀毒软件误报。

---

**基于 参考项目实战经验优化，助你打造商业级安装包！**

## UV Package Manager

<!-- source: wshobson/agents plugins/python-development/skills/uv-package-manager/SKILL.md -->

Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows.

### When to Use This Skill

- Setting up new Python projects quickly
- Managing Python dependencies faster than pip
- Creating and managing virtual environments
- Installing Python interpreters
- Resolving dependency conflicts efficiently
- Migrating from pip/pip-tools/poetry
- Speeding up CI/CD pipelines
- Managing monorepo Python projects
- Working with lockfiles for reproducible builds
- Optimizing Docker builds with Python dependencies

### Core Concepts

#### 1. What is uv?

- **Ultra-fast package installer**: 10-100x faster than pip
- **Written in Rust**: Leverages Rust's performance
- **Drop-in pip replacement**: Compatible with pip workflows
- **Virtual environment manager**: Create and manage venvs
- **Python installer**: Download and manage Python versions
- **Resolver**: Advanced dependency resolution
- **Lockfile support**: Reproducible installations

#### 2. Key Features

- Blazing fast installation speeds
- Disk space efficient with global cache
- Compatible with pip, pip-tools, poetry
- Comprehensive dependency resolution
- Cross-platform support (Linux, macOS, Windows)
- No Python required for installation
- Built-in virtual environment support

#### 3. UV vs Traditional Tools

- **vs pip**: 10-100x faster, better resolver
- **vs pip-tools**: Faster, simpler, better UX
- **vs poetry**: Faster, less opinionated, lighter
- **vs conda**: Faster, Python-focused

### Installation

#### Quick Install

```bash
# Using Homebrew (macOS or Linux)
brew install uv

# Using Cargo (if you have Rust)
cargo install --locked uv
```

On Windows, use WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Use the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/)
for other supported installation methods.

#### Verify Installation

```bash
uv --version
# uv 0.x.x
```

### Quick Start

#### Create a New Project

```bash
# Create new project with virtual environment
uv init my-project
cd my-project

# Or create in current directory
uv init .

# Initialize creates:
# - .python-version (Python version)
# - pyproject.toml (project config)
# - README.md
# - .gitignore
```

#### Install Dependencies

```bash
# Install packages (creates venv if needed)
uv add requests pandas

# Install dev dependencies
uv add --dev pytest black ruff

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv sync
```

### Virtual Environment Management

#### Pattern 1: Creating Virtual Environments

```bash
# Create virtual environment with uv
uv venv

# Create with specific Python version
uv venv --python 3.12

# Create with custom name
uv venv my-env

# Create with system site packages
uv venv --system-site-packages

# Specify location
uv venv /path/to/venv
```

#### Pattern 2: Activating Virtual Environments

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Or use uv run (no activation needed)
uv run python script.py
uv run pytest
```

#### Pattern 3: Using uv run

```bash
# Run Python script (auto-activates venv)
uv run python app.py

# Run installed CLI tool
uv run black .
uv run pytest

# Run with specific Python version
uv run --python 3.11 python script.py

# Pass arguments
uv run python script.py --arg value
```

### Package Management

#### Pattern 4: Adding Dependencies

```bash
# Add package (adds to pyproject.toml)
uv add requests

# Add with version constraint
uv add "django>=4.0,<5.0"

# Add multiple packages
uv add numpy pandas matplotlib

# Add dev dependency
uv add --dev pytest pytest-cov

# Add optional dependency group
uv add --optional docs sphinx

# Add from git
uv add git+https://github.com/user/repo.git

# Add from git with specific ref
uv add git+https://github.com/user/repo.git@v1.0.0

# Add from local path
uv add ./local-package

# Add editable local package
uv add -e ./local-package
```

#### Pattern 5: Removing Dependencies

```bash
# Remove package
uv remove requests

# Remove dev dependency
uv remove --dev pytest

# Remove multiple packages
uv remove numpy pandas matplotlib
```

#### Pattern 6: Upgrading Dependencies

```bash
# Upgrade specific package
uv add --upgrade requests

# Upgrade all packages
uv sync --upgrade

# Upgrade package to latest
uv add --upgrade requests

# Show what would be upgraded
uv tree --outdated
```

#### Pattern 7: Locking Dependencies

```bash
# Generate uv.lock file
uv lock

# Update lock file
uv lock --upgrade

# Lock without installing
uv lock --no-install

# Lock specific package
uv lock --upgrade-package requests
```

### Python Version Management

#### Pattern 8: Installing Python Versions

```bash
# Install Python version
uv python install 3.12

# Install multiple versions
uv python install 3.11 3.12 3.13

# Install latest version
uv python install

# List installed versions
uv python list

# Find available versions
uv python list --all-versions
```

#### Pattern 9: Setting Python Version

```bash
# Set Python version for project
uv python pin 3.12

# This creates/updates .python-version file

# Use specific Python version for command
uv --python 3.11 run python script.py

# Create venv with specific version
uv venv --python 3.12
```

### Project Configuration

#### Pattern 10: pyproject.toml with uv

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    # Additional dev dependencies managed by uv
]

[tool.uv.sources]
# Custom package sources
my-package = { git = "https://github.com/user/repo.git" }
```

#### Pattern 11: Using uv with Existing Projects

```bash
# Migrate from requirements.txt
uv add -r requirements.txt

# Migrate from poetry
# Already have pyproject.toml, just use:
uv sync

# Export to requirements.txt
uv pip freeze > requirements.txt

# Export with hashes
uv pip freeze --require-hashes > requirements.txt
```

For advanced workflows including Docker integration, lockfile management, performance optimization, tool comparison, common workflows, tool integration, troubleshooting, best practices, migration guides, and command reference, see references/advanced-patterns.md

## UV Package Manager — Advanced Reference

<!-- source: wshobson/agents plugins/python-development/skills/uv-package-manager/references/advanced-patterns.md -->

Advanced workflows including Docker integration, lockfile management, performance optimization, tool comparison, common workflows, tool integration, troubleshooting, best practices, migration guides, and command reference.

### Advanced Workflows

#### Pattern 12: Monorepo Support

```bash
# Project structure
# monorepo/
#   packages/
#     package-a/
#       pyproject.toml
#     package-b/
#       pyproject.toml
#   pyproject.toml (root)

# Root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

# Install all workspace packages
uv sync

# Add workspace dependency
uv add --path ./packages/package-a
```

#### Pattern 13: CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v2
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run tests
        run: uv run pytest

      - name: Run linting
        run: |
          uv run ruff check .
          uv run black --check .
```

#### Pattern 14: Docker Integration

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Run application
CMD ["uv", "run", "python", "app.py"]
```

**Optimized multi-stage build:**

```dockerfile
# Multi-stage Dockerfile
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies to venv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy venv from builder
COPY --from=builder /app/.venv .venv
COPY . .

# Use venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "app.py"]
```

#### Pattern 15: Lockfile Workflows

```bash
# Create lockfile (uv.lock)
uv lock

# Install from lockfile (exact versions)
uv sync --frozen

# Update lockfile without installing
uv lock --no-install

# Upgrade specific package in lock
uv lock --upgrade-package requests

# Check if lockfile is up to date
uv lock --check

# Export lockfile to requirements.txt
uv export --format requirements-txt > requirements.txt

# Export with hashes for security
uv export --format requirements-txt --hash > requirements.txt
```

### Performance Optimization

#### Pattern 16: Using Global Cache

```bash
# UV automatically uses global cache at:
# Linux: ~/.cache/uv
# macOS: ~/Library/Caches/uv
# Windows: %LOCALAPPDATA%\uv\cache

# Clear cache
uv cache clean

# Check cache size
uv cache dir
```

#### Pattern 17: Parallel Installation

```bash
# UV installs packages in parallel by default

# Control parallelism
uv pip install --jobs 4 package1 package2

# No parallel (sequential)
uv pip install --jobs 1 package
```

#### Pattern 18: Offline Mode

```bash
# Install from cache only (no network)
uv pip install --offline package

# Sync from lockfile offline
uv sync --frozen --offline
```

### Comparison with Other Tools

#### uv vs pip

```bash
# pip
python -m venv .venv
source .venv/bin/activate
pip install requests pandas numpy
# ~30 seconds

# uv
uv venv
uv add requests pandas numpy
# ~2 seconds (10-15x faster)
```

#### uv vs poetry

```bash
# poetry
poetry init
poetry add requests pandas
poetry install
# ~20 seconds

# uv
uv init
uv add requests pandas
uv sync
# ~3 seconds (6-7x faster)
```

#### uv vs pip-tools

```bash
# pip-tools
pip-compile requirements.in
pip-sync requirements.txt
# ~15 seconds

# uv
uv lock
uv sync --frozen
# ~2 seconds (7-8x faster)
```

### Common Workflows

#### Pattern 19: Starting a New Project

```bash
# Complete workflow
uv init my-project
cd my-project

# Set Python version
uv python pin 3.12

# Add dependencies
uv add fastapi uvicorn pydantic

# Add dev dependencies
uv add --dev pytest black ruff mypy

# Create structure
mkdir -p src/my_project tests

# Run tests
uv run pytest

# Format code
uv run black .
uv run ruff check .
```

#### Pattern 20: Maintaining Existing Project

```bash
# Clone repository
git clone https://github.com/user/project.git
cd project

# Install dependencies (creates venv automatically)
uv sync

# Install with dev dependencies
uv sync --all-extras

# Update dependencies
uv lock --upgrade

# Run application
uv run python app.py

# Run tests
uv run pytest

# Add new dependency
uv add new-package

# Commit updated files
git add pyproject.toml uv.lock
git commit -m "Add new-package dependency"
```

### Tool Integration

#### Pattern 21: Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-lock
        name: uv lock
        entry: uv lock
        language: system
        pass_filenames: false

      - id: ruff
        name: ruff
        entry: uv run ruff check --fix
        language: system
        types: [python]

      - id: black
        name: black
        entry: uv run black
        language: system
        types: [python]
```

#### Pattern 22: VS Code Integration

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-v"],
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

### Troubleshooting

#### Common Issues

```bash
# Issue: uv not found
# Solution: Add to PATH or reinstall
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Issue: Wrong Python version
# Solution: Pin version explicitly
uv python pin 3.12
uv venv --python 3.12

# Issue: Dependency conflict
# Solution: Check resolution
uv lock --verbose

# Issue: Cache issues
# Solution: Clear cache
uv cache clean

# Issue: Lockfile out of sync
# Solution: Regenerate
uv lock --upgrade
```

### Best Practices

#### Project Setup

1. **Always use lockfiles** for reproducibility
2. **Pin Python version** with .python-version
3. **Separate dev dependencies** from production
4. **Use uv run** instead of activating venv
5. **Commit uv.lock** to version control
6. **Use --frozen in CI** for consistent builds
7. **Leverage global cache** for speed
8. **Use workspace** for monorepos
9. **Export requirements.txt** for compatibility
10. **Keep uv updated** for latest features

#### Performance Tips

```bash
# Use frozen installs in CI
uv sync --frozen

# Use offline mode when possible
uv sync --offline

# Parallel operations (automatic)
# uv does this by default

# Reuse cache across environments
# uv shares cache globally

# Use lockfiles to skip resolution
uv sync --frozen  # skips resolution
```

### Migration Guide

#### From pip + requirements.txt

```bash
# Before
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# After
uv venv
uv pip install -r requirements.txt
# Or better:
uv init
uv add -r requirements.txt
```

#### From Poetry

```bash
# Before
poetry install
poetry add requests

# After
uv sync
uv add requests

# Keep existing pyproject.toml
# uv reads [project] and [tool.poetry] sections
```

#### From pip-tools

```bash
# Before
pip-compile requirements.in
pip-sync requirements.txt

# After
uv lock
uv sync --frozen
```

### Command Reference

#### Essential Commands

```bash
# Project management
uv init [PATH]              # Initialize project
uv add PACKAGE              # Add dependency
uv remove PACKAGE           # Remove dependency
uv sync                     # Install dependencies
uv lock                     # Create/update lockfile

# Virtual environments
uv venv [PATH]              # Create venv
uv run COMMAND              # Run in venv

# Python management
uv python install VERSION   # Install Python
uv python list              # List installed Pythons
uv python pin VERSION       # Pin Python version

# Package installation (pip-compatible)
uv pip install PACKAGE      # Install package
uv pip uninstall PACKAGE    # Uninstall package
uv pip freeze               # List installed
uv pip list                 # List packages

# Utility
uv cache clean              # Clear cache
uv cache dir                # Show cache location
uv --version                # Show version
```
