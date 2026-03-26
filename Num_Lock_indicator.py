#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import threading
import time
import os
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem, Menu


class NumLockIndicator:
    def __init__(self):
        self.icon = None
        self.running = True
        self.current_state = None
        self.check_interval = 0.5
        self.font_large = None
        self.font_small = None
        
        self._init_font()

    def _init_font(self):
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
                print(f"Font loaded successfully: {fp}")
                break
        
        if font_path:
            try:
                self.font_small = ImageFont.truetype(font_path, 22)
                self.font_large = ImageFont.truetype(font_path, 28)
            except Exception as e:
                pass
        
        if self.font_small is None:
            default_font = ImageFont.load_default()
            self.font_small = default_font
            self.font_large = default_font
            print("Use the default font")

    def get_num_lock_state(self):
        try:
            result = subprocess.run(
                ['xset', 'q'], 
                capture_output=True, 
                text=True,
                timeout=1
            )
            for line in result.stdout.split('\n'):
                if 'Num Lock:' in line:
                    parts = line.split('Num Lock:')
                    if len(parts) > 1:
                        status = parts[1].split()[0].strip().lower()
                        return status == 'on'
        except Exception:
            pass
        return False
    
    def create_rounded_rectangle(self, size, radius, color):
        width, height = size
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)], 
            radius=radius, 
            fill=color
        )
        return image
    
    def create_icon_image(self, is_num_on):
        width, height = 64, 64
        corner_radius = 12
        
        bg_color = (220, 50, 50) if is_num_on else (50, 150, 50)
        text_color = (255, 255, 255)
        
        image = self.create_rounded_rectangle((width, height), corner_radius, bg_color + (255,))
        draw = ImageDraw.Draw(image)
        
        if is_num_on:
            text = "123"  
            font = self.font_small  
        else:
            text = "arr"  
            font = self.font_large 
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 2
        
        draw.text((x, y), text, font=font, fill=text_color)
        
        return image
    
    def update_icon(self):
        
        state = self.get_num_lock_state()
        
        if state != self.current_state:
            self.current_state = state
            new_icon = self.create_icon_image(state)
            
            if self.icon:
                self.icon.icon = new_icon
                self.icon.title = "Num Lock: 123" if state else "Num Lock: arr"
    
    def monitor_loop(self):
        while self.running:
            self.update_icon()
            time.sleep(self.check_interval)
    
    def on_quit(self, icon, item):
        self.running = False
        icon.stop()
    
    def run(self):
        initial_state = self.get_num_lock_state()
        self.current_state = initial_state
        
        initial_icon = self.create_icon_image(initial_state)
        
        menu = Menu(
            MenuItem("stop", self.on_quit)
        )
        
        self.icon = pystray.Icon(
            "numlock_indicator",
            initial_icon,
            "Num Lock: 123" if initial_state else "Num Lock: arr",
            menu
        )
        
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        self.icon.run()


if __name__ == "__main__":
    indicator = NumLockIndicator()
    indicator.run()
