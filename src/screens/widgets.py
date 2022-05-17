import tkinter as tk
# from tkinter import ttk
import subprocess

class Widget(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.main_frame = tk.Frame(self, bg = '#272727', height = 800, width = 1000)
        self.main_frame.grid(row=0, column=0, sticky='nswe')

class ControllPanel(Widget):

    def __init__(self, parent, controller):
        Widget.__init__(self, parent)

        self.controller = controller

        self.splash_container = controller._get_splash_container()

        frame1 = tk.LabelFrame(self.main_frame, text = 'Running processes', width = 500, height = 400)
        frame1.grid(column = 0, row = 0, sticky='nsew')

        frame2 = tk.LabelFrame(self.main_frame, text='Docker logs', width = 500, height = 400)
        frame2.grid(column = 1, row = 0, sticky = 'nswe')

        frame3 = tk.LabelFrame(self.main_frame, bg = 'green', text = 'Control panel', width = 500, height = 400)
        frame3.grid(column = 0, row = 1, sticky='nswe')

        self.listbox = tk.Listbox(frame1, width=100)

        for i in range(20):
            self.listbox.insert("end", f"TIME=00:00:00 12:35:33, PID={i}, STATUS=running, PARAMS=default")

        self.listbox.pack(side = 'left', fill='both', expand = True)

        start_splash_button = tk.Button(frame2, text = 'start splash', command = self.start_splash)
        start_splash_button.pack()

        stop_splash_button = tk.Button(frame2, text = 'stop splash', command= self.stop_splash)
        stop_splash_button.pack()

        log_splash_button = tk.Button(frame2, text = 'clear logs', command= self.clear_log)
        log_splash_button.pack()

        start_scraper = tk.Button(frame2, text = 'start scraper', command = self.start_scraper) 
        start_scraper.pack()

        self.docker_running_status_label = tk.Label(frame2, text='Getting ready ... ')
        self.docker_running_status_label.pack(side = 'top')

        self.docker_status = None
        
        self.main_frame.after(1000, self.loop)
    
    def test_callback(self):
        print("test callback called")
    
    def start_scraper(self):
        # self.controller._start_scraper_async()
        self.controller._start_scraper()
    
    def loop(self):
        status = self.splash_container.is_running()

        if status != self.docker_status:
            self.docker_status = status
            self.toggle_docker_status(self.docker_status)

        self.main_frame.after(1000, self.loop)

    
    def toggle_docker_status(self, is_running):
        if is_running:
            self.docker_running_status_label.config(text = "Splash status: RUNNING")
        else:
            self.docker_running_status_label.config(text = "Splash status: NOT RUNNING")

    def start_splash(self):
        if self.splash_container.is_running() == False:
            print("Starting splash")
            self.splash_container.start()
        else:
            print("Splash is already running")

    def stop_splash(self):
        if self.splash_container.is_running() == True:
            self.splash_container.stop()
    
    def get_running_spider_logs(self):
        return self.controller._get_logs()

    def clear_log(self):
        self.listbox.delete(0, 'end')

    def add_log(self, text):
        self.listbox.insert('end', text)

class AnotherPanel(Widget):
    def __init__(self, parent):
        Widget.__init__(self, parent)
        label = tk.Label(self.main_frame, text = 'Label 1')
        label.pack(side = 'top')