# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 05:54:47 2024

@author: IAN CARTER KULANI
"""

import tkinter as tk
from tkinter import messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import random

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Traffic Monitoring Tool")

        # User input for IP address
        self.ip_label = tk.Label(root, text="Enter IP Address for Monitoring:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(root, width=30)
        self.ip_entry.pack()

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack()

        # Result and Traffic Display Area
        self.result_label = tk.Label(root, text="Traffic Data Will Appear Here...")
        self.result_label.pack()

        # Graph Setup for Reporting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Traffic Data for Analytics
        self.time_series = []
        self.inbound_series = []
        self.outbound_series = []
        self.traffic_types = {'VoIP': 0, 'Video Streaming': 0, 'General Traffic': 0}

        # Monitoring state variables
        self.monitoring_thread = None
        self.is_monitoring = False

        # Traffic shaping parameters (simulated)
        self.qos_policy = {'VoIP': 40, 'Video Streaming': 30, 'General Traffic': 30}

    def start_monitoring(self):
        ip_address = self.ip_entry.get()
        
        if not ip_address:
            messagebox.showerror("Input Error", "Please enter a valid IP address.")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self.monitor_traffic, args=(ip_address,))
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

        self.result_label.config(text=f"Monitoring traffic for IP: {ip_address}")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
    def monitor_traffic(self, ip_address):
        try:
            while self.is_monitoring:
                # Simulate traffic data for different types (for QoS)
                net_stats = psutil.net_io_counters()
                inbound = net_stats.bytes_recv
                outbound = net_stats.bytes_sent

                # Update traffic metrics and apply QoS policies (simulated)
                self.apply_qos_policy(inbound, outbound)

                # Capture the time and traffic values
                current_time = time.time()
                self.time_series.append(current_time)
                self.inbound_series.append(inbound)
                self.outbound_series.append(outbound)

                # Update the graph every second
                self.ax.clear()
                self.ax.plot(self.time_series, self.inbound_series, label="Inbound Traffic", color='g')
                self.ax.plot(self.time_series, self.outbound_series, label="Outbound Traffic", color='r')
                self.ax.set_xlabel("Time (seconds)")
                self.ax.set_ylabel("Bytes")
                self.ax.legend(loc="upper left")
                self.canvas.draw()

                # Sleep for 1 second before updating again
                time.sleep(1)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while monitoring traffic: {e}")

    def apply_qos_policy(self, inbound, outbound):
        # Simulate traffic shaping: prioritize traffic based on QoS policy
        voip_bandwidth = self.qos_policy['VoIP'] / 100 * inbound
        video_bandwidth = self.qos_policy['Video Streaming'] / 100 * outbound
        general_bandwidth = (self.qos_policy['General Traffic'] / 100) * (inbound + outbound)

        # Update traffic types (Simulating QoS bandwidth allocation)
        self.traffic_types['VoIP'] += voip_bandwidth
        self.traffic_types['Video Streaming'] += video_bandwidth
        self.traffic_types['General Traffic'] += general_bandwidth

    def stop_monitoring(self):
        self.is_monitoring = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join()

        # Show Summary after monitoring stops
        self.show_summary_charts()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def show_summary_charts(self):
        # Pie chart showing traffic distribution (VoIP, Video Streaming, General Traffic)
        traffic_labels = list(self.traffic_types.keys())
        traffic_sizes = list(self.traffic_types.values())

        # Creating Pie Chart for Traffic Distribution
        fig1, ax1 = plt.subplots()
        ax1.pie(traffic_sizes, labels=traffic_labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral', 'lightblue'])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("Traffic Distribution by Type (QoS)")

        # Show the Pie chart
        plt.show()

        # Bar chart showing total traffic (inbound vs outbound)
        fig2, ax2 = plt.subplots()
        ax2.bar(['Inbound Traffic', 'Outbound Traffic'], [sum(self.inbound_series), sum(self.outbound_series)], color=['green', 'red'])
        ax2.set_ylabel('Bytes')
        ax2.set_title('Total Traffic Volume')

        # Show the Bar chart
        plt.show()

        # Line chart for time-series data (inbound vs outbound over time)
        fig3, ax3 = plt.subplots()
        ax3.plot(self.time_series, self.inbound_series, label="Inbound Traffic", color='green')
        ax3.plot(self.time_series, self.outbound_series, label="Outbound Traffic", color='red')
        ax3.set_xlabel("Time (seconds)")
        ax3.set_ylabel("Bytes")
        ax3.set_title("Inbound vs Outbound Traffic Over Time")
        ax3.legend(loc="upper left")

        # Show the Line chart
        plt.show()

def main():
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
