import tkinter as tk
import calendar
from datetime import datetime
root =tk.Tk()
root.title("Calender")
root.geometry("300x300")
root.resizable(False, False)
root.configure(bg="skyblue")

now = datetime.now()
year = now.year 
month =now.month
cal_text =calendar.month(year, month)    

label = tk.Label(root, text=cal_text, font=("Consolas",14), bg="skyblue", fg="black")
label.pack(pady=20)




root.mainloop()