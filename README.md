# Ubuntu_case_toggle_and_number_key_toggle_display_component

Ubuntu 系统托盘指示器，实时显示 **Caps Lock（大小写锁定）** 和 **Num Lock（数字键盘锁定）** 状态。

## 功能特性

- 🔴 **Caps Lock 指示器**：大写显示红色 "MAX"，小写显示绿色 "min"
- 🔴 **Num Lock 指示器**：数字模式显示红色 "123"，方向键模式显示绿色 "arr"
- 🖥️ **系统托盘显示**：圆角图标设计，统一视觉大小
- ⚡ **实时监测**：每 0.5 秒自动检测状态变化
- 🖱️ **右键菜单**：支持右键退出程序

## 项目文件

| 文件 | 说明 |
|------|------|
| `capslock_indicator.py` | Caps Lock 状态指示器 |
| `Num_Lock_indicator.py` | Num Lock 状态指示器 |

## 使用方法

### 1. 安装依赖

  ```bash
  pip3 install pystray pillow

### 2. 系统依赖（Ubuntu）
  
  ```bash
  sudo apt-get install python3-pil.imagetk x11-xserver-utils

### 3. 编译可执行文件
  ```bash
  pyinstaller --onefile --windowed --name <"生成的可执行文件名称"> <"可执行文件名称">

### 4. 使用编译后的程

  ```bash
  ./dist/capslock-indicator
  ./dist/numlock-indicator
