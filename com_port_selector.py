import tkinter as tk
import serial.tools.list_ports
from cvs_stuff import *

def get_list_of_com_ports():
    list_of_ports = []
    list_of_ports_raw = []
    ports = serial.tools.list_ports.comports()
    
    for port, desc, hwid in sorted(ports):
        a = ("{}: {}".format(port, desc))
        list_of_ports.append(a)
        list_of_ports_raw.append(port)
    return(list_of_ports,list_of_ports_raw)

def save_com_info(baud_val,com_val,list_of_ports,list_of_ports_raw,root):
    filename = "com_settings.csv"
    try:
        com_index_val = list_of_ports.index(com_val)
    except:
        pass
    com_name = list_of_ports_raw[com_index_val]
    li = [com_name,str(baud_val)]
    add_record(filename,li)
    root.quit()

def main_frame(root):
    for widget in root.winfo_children():
        widget.destroy()
    list_of_ports,list_of_ports_raw = get_list_of_com_ports()
    # List of COM ports and baud rates
    if len(list_of_ports) == 0:
        com_ports = ["None"]
    else:
        com_ports = list_of_ports
    baud_rates = [300, 1200, 2400, 4800, 9600]

    # Create dropdown for COM ports
    com_var = tk.StringVar(root)
    com_var.set(com_ports[0])  # default value
    com_dropdown = tk.OptionMenu(root, com_var, *com_ports)
    com_dropdown.grid(row=0, column=0, padx=10, pady=10)

    # Create dropdown for baud rates
    baud_var = tk.StringVar(root)
    baud_var.set(baud_rates[0])  # default value
    baud_dropdown = tk.OptionMenu(root, baud_var, *baud_rates)
    baud_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Create save and exit button
    tk.Button(root, text="Save and Exit", command=lambda:save_com_info(baud_val=baud_var.get(),com_val=com_var.get(),list_of_ports=list_of_ports,list_of_ports_raw=list_of_ports_raw,root=root)).grid(row=1, column=0, padx=10, pady=10)

    # Create exit button
    tk.Button(root, text="Exit", command=root.quit).grid(row=1, column=1, padx=10, pady=10)

def run_com_select_window():
    root = tk.Tk()
    root.title("COM Port and Baud Rate Selection")
    root.geometry("400x200")
    main_frame(root)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("COM Port and Baud Rate Selection")
    root.geometry("400x200")
    main_frame(root)
    root.mainloop()
