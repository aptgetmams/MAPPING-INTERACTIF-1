#!/usr/bin/env python3

import psutil
import time
import threading

class PerformanceMonitor:
    def __init__(self):
        self.running = False
        
    def monitor_loop(self):
        while self.running:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            temp = self.get_cpu_temp()
            
            print(f"CPU: {cpu}% | RAM: {memory}% | Temp: {temp}°C")
            time.sleep(5)
            
    def get_cpu_temp(self):
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000
                return round(temp, 1)
        except:
            return 0
            
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop)
        self.thread.start()
        
    def stop(self):
        self.running = False
