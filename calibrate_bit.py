import tkinter as tk
from adapter import *
from cvs_stuff import *

port = ""
baudrate = 0

max_val = 0
min_val = 0
filename = "max_min.csv"


def get_com_vals():
    global port
    global baudrate
    val = read_record("com_settings.csv")
    port = val[0][0]
    baudrate = int(val[0][1])

def pull_hand_down_get_val():
    global max_val
    li = []
    for i in range(50):
        li.append(read_com_port(port,baudrate))
    max_val = max(li)    
         

def hand_up_val():
    global min_val
    li = []
    for i in range(50):
        li.append(read_com_port(port,baudrate))
    min_val = min(li)    
         

def save_val_info():
    lis = [max_val,min_val]
    add_record(filename, lis)
    display_records(filename)
    


def start_frame(root):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Button(root, text="Start Calibration", command=lambda: pull_handbrake_frame(root)).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

def pull_handbrake_frame(root):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Pull handbrake down").pack(pady=10)
    tk.Button(root, text="Done", command=lambda: let_handbrake_go_frame(root)).pack(pady=10)

def let_handbrake_go_frame(root):
    pull_hand_down_get_val()
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Let handbrake go").pack(pady=10)
    tk.Button(root, text="Done", command=lambda: calibration_complete_frame(root)).pack(pady=10)

def calibration_complete_frame(root):
    hand_up_val()
    save_val_info()
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Calibration complete").pack(pady=10)
    tk.Button(root, text="Close", command=root.quit).pack(pady=10)

def import_bit():
    get_com_vals()
    root = tk.Tk()
    root.title("Calibration App")
    root.geometry("300x200")
    start_frame(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calibration App")
    root.geometry("300x200")
    start_frame(root)
    root.mainloop()
