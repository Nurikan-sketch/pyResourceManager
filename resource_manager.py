import psutil
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import timedelta
import subprocess

def get_network_usage():
    net_io = psutil.net_io_counters()
    return f"Sent: {net_io.bytes_sent / 1024**2:.2f} MB, Received: {net_io.bytes_recv / 1024**2:.2f} MB"


def get_cpu_temperature():
    try:
        result = subprocess.run(['smctemp', '-c'], capture_output=True, text=True, timeout=0.5)
        temp = result.stdout.strip()
        return f"CPU Temp: {temp}"
    except Exception as e:
        return f"Temperature: Error ({str(e)})"

def get_gpu_temperature():
    try:
        result = subprocess.run(['smctemp', '-g'], capture_output=True, text=True, timeout=0.5)
        temp = result.stdout.strip()
        return f"GPU Temp: {temp}"
    except Exception as e:
        return f"Temperature: Error ({str(e)})"

def get_gpu_usage():
    try:
        gpu_usage = psutil.cpu_percent(percpu=True)[0]
        return f"GPU Usage: {gpu_usage:.1f}%"
    except Exception as e:
        return f"GPU Usage: Error ({str(e)})"

def update_system_usage():
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_time_left = battery.secsleft
            time_left = timedelta(seconds=battery_time_left)

            if battery.power_plugged:
                battery_status = "Charging"
            else:
                battery_status = "Discharging"

            battery_percent_label.config(text=f"Battery: {psutil.sensors_battery().percent}%")
            battery_time_left_label.config(text=f"Time left: {time_left}")
            battery_status_label.config(text=f"Status: {battery_status}")
    
        else:
            battery_percent_label.config(text="Battery: Not detected")
            battery_time_left_label.config(text="Time left: N/A")
            battery_status_label.config(text="Status: N/A")
    except Exception as e:
        print(f"Error getting battery info: {e}")

    memory_info = psutil.virtual_memory()
    memory_usage_percent = memory_info.percent
    memory_total_gb = memory_info.total / (1024 ** 3)
    memory_used_gb = memory_info.used / (1024 ** 3)

    cpu_usage_label.config(text=f"CPU Usage: {psutil.cpu_percent(interval=0.5)}%")
    gpu_usage_label.config(text=get_gpu_usage())
    memory_label.config(text=f"RAM Usage: {memory_usage_percent}%")
    total_memory_label.config(text=f"RAM total: {memory_total_gb:.2f} GB")
    used_memory_label.config(text=f"RAM used: {memory_used_gb:.2f} GB")

    network_label.config(text=f"Network: {get_network_usage()}")

    cpu_temp_label.config(text=get_cpu_temperature())
    gpu_temp_label.config(text=get_gpu_temperature())


    root.after(500, update_system_usage)


root = tk.Tk()
root.title("Monitoring")
root.geometry("400x400")

padding = 5;

ttk.Label(root, text=f"CPU: Apple M3 Pro {psutil.cpu_count()} Cores", font=("Arial", 12)).pack(pady=5)

cpu_usage_label = ttk.Label(root, text="CPU Usage: ", font=("Arial", 12))
cpu_usage_label.pack(pady=5)

cpu_temp_label = ttk.Label(root, text="CPU Temp: ", font=("Arial", 12))
cpu_temp_label.pack(pady=5)

padding += 5;

gpu_usage_label = ttk.Label(root, text="GPU Usage: ", font=("Arial", 12))
gpu_usage_label.pack(pady=5)

gpu_temp_label = ttk.Label(root, text="GPU Temp: ", font=("Arial", 12))
gpu_temp_label.pack(pady=5)

padding += 5;

memory_label = ttk.Label(root, text="RAM Usage: ", font=("Arial", 12))
memory_label.pack(pady=5)

total_memory_label = ttk.Label(root, text="RAM total: ", font=("Arial", 12))
total_memory_label.pack(pady=5)

used_memory_label = ttk.Label(root, text="RAM used: ", font=("Arial", 12))
used_memory_label.pack(pady=5)

padding += 5;

battery_percent_label = ttk.Label(root, text="Battery: ", font=("Arial", 12))
battery_percent_label.pack(pady=5)

battery_time_left_label = ttk.Label(root, text="Time left: ", font=("Arial", 12))
battery_time_left_label.pack(pady=5)

battery_status_label = ttk.Label(root, text="Status: ", font=("Arial", 12))
battery_status_label.pack(pady=5)

network_label = ttk.Label(root, text="Network: ", font=("Arial", 12))
network_label.pack(pady=5)


update_system_usage()


root.mainloop()