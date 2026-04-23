#Digital clock
import tkinter as tk
import time

# Create window
root = tk.Tk()
root.title("Digital Clock")
root.geometry("350x150")
root.resizable(False, False)
root.configure(bg="black")

# Time label
label = tk.Label(root, font=("Digital-7", 48), bg="black", fg="cyan")
label.pack(pady=20)

def update_time():
    current_time = time.strftime("%H:%M:%S")
    label.config(text=current_time)
    root.after(1000, update_time)     # Update every 1 sec

update_time()  # Call function first time

root.mainloop()
