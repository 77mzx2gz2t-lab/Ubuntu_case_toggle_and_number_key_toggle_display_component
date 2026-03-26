#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caps Lock 系统托盘指示器
- 大写显示 "MAX" 图标（红色圆角）
- 小写显示 "min" 图标（绿色圆角）
- 统一视觉大小：大写用小字号，小写用大字号，使整体尺寸一致
"""

import subprocess
import threading
import time
import os
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem, Menu


class CapsLockIndicator:
    def __init__(self):
        self.icon = None
        self.running = True
        self.current_state = None
        self.check_interval = 0.5
        self.font_large = None
        self.font_small = None
        
        # 初始化时加载字体
        self._init_font()

    def _init_font(self):
        """加载字体，准备两种字号以统一视觉大小"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/mnt/c/Windows/Fonts/arialbd.ttf",
        ]
        
        font_path = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_path = fp
                print(f"成功加载字体: {fp}")
                break
        
        if font_path:
            try:
                # 大写 "MAX" 用小字号（因为字母本身就大）
                self.font_small = ImageFont.truetype(font_path, 24)
                # 小写 "min" 用大字号（因为字母本身就小）
                self.font_large = ImageFont.truetype(font_path, 32)
            except Exception as e:
                pass
        
        # 如果加载失败，使用默认字体
        if self.font_small is None:
            default_font = ImageFont.load_default()
            self.font_small = default_font
            self.font_large = default_font
            print("使用默认字体")

    def get_caps_lock_state(self):
        """获取 Caps Lock 状态"""
        try:
            result = subprocess.run(
                ['xset', 'q'], 
                capture_output=True, 
                text=True,
                timeout=1
            )
            for line in result.stdout.split('\n'):
                if 'Caps Lock:' in line:
                    parts = line.split('Caps Lock:')
                    if len(parts) > 1:
                        status = parts[1].split()[0].strip().lower()
                        return status == 'on'
        except Exception:
            pass
        return False
    
    def create_rounded_rectangle(self, size, radius, color):
        """创建圆角矩形图像"""
        width, height = size
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)], 
            radius=radius, 
            fill=color
        )
        return image
    
    def create_icon_image(self, is_caps_on):
        """生成图标 - 统一 MAX 和 min 的视觉大小"""
        width, height = 64, 64
        corner_radius = 12
        
        # 颜色：大写=红色，小写=绿色
        bg_color = (220, 50, 50) if is_caps_on else (50, 150, 50)
        text_color = (255, 255, 255)
        
        # 创建圆角背景
        image = self.create_rounded_rectangle((width, height), corner_radius, bg_color + (255,))
        draw = ImageDraw.Draw(image)
        
        # 根据状态选择文字和字体
        if is_caps_on:
            text = "MAX"
            font = self.font_small  # 大写字母用小字号
        else:
            text = "min"
            font = self.font_large  # 小写字母用大字号
        
        # 计算文字居中位置
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 2
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=text_color)
        
        return image
    
    def update_icon(self):
        """更新托盘图标"""
        state = self.get_caps_lock_state()
        
        if state != self.current_state:
            self.current_state = state
            new_icon = self.create_icon_image(state)
            
            if self.icon:
                self.icon.icon = new_icon
                self.icon.title = "Caps Lock: MAX (大写)" if state else "Caps Lock: min (小写)"
    
    def monitor_loop(self):
        """后台监控线程"""
        while self.running:
            self.update_icon()
            time.sleep(self.check_interval)
    
    def on_quit(self, icon, item):
        """退出程序"""
        self.running = False
        icon.stop()
    
    def run(self):
        """启动指示器"""
        initial_state = self.get_caps_lock_state()
        self.current_state = initial_state
        
        initial_icon = self.create_icon_image(initial_state)
        
        menu = Menu(
            MenuItem("退出", self.on_quit)
        )
        
        self.icon = pystray.Icon(
            "capslock_indicator",
            initial_icon,
            "Caps Lock: MAX (大写)" if initial_state else "Caps Lock: min (小写)",
            menu
        )
        
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        self.icon.run()


if __name__ == "__main__":
    indicator = CapsLockIndicator()
    indicator.run()