import time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("进程控制")
        self.running_thread = None

        self.output_text = tk.Text(root)
        self.output_text.pack()

        self.start_button = tk.Button(root, text="开始进程", command=self.start_process)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="停止进程", command=self.stop_process)
        self.stop_button.pack(pady=10)

    def start_process(self):
        if self.running_thread is None or not self.running_thread.running():
            self.running_thread = MyThreadPoolExecutor(self)
            self.running_thread.start()
            self.root.after(0, self.check_status)
            messagebox.showinfo("信息", "进程已启动！")
        else:
            messagebox.showwarning("警告", "进程已经在运行！")

    def stop_process(self):
        if self.running_thread is not None and self.running_thread.running():
            self.running_thread.stop()
            self.running_thread.join()
            messagebox.showinfo("信息", "进程已停止！")
        else:
            messagebox.showwarning("警告", "没有正在运行的进程！")

    def update_text(self, text):
        self.root.after(0, self.output_text.insert, tk.END, text + "\n")

    def check_status(self):
        if self.running_thread is not None:
            if self.running_thread.running():
                self.root.after(1000, self.check_status)
            else:
                messagebox.showinfo("信息", "进程已完成！")

class MyThreadPoolExecutor:
    def __init__(self, app):
        self.app = app
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None

    def start(self):
        self.future = self.executor.submit(self.run)

    def run(self):
        for i in range(5):  # Simulate some work
            print("Processing...")
            self.app.update_text("Processing...")
            time.sleep(1)

    def stop(self):
        if self.future is not None:
            self.future.cancel()

    def running(self):
        return self.future is not None and not self.future.done()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
