# alarm_gui.py
# Simple GUI alarm with set, cancel and snooze.
# Requires Python built-in tkinter. Optional playsound for mp3/wav.

import tkinter as tk
from datetime import datetime
import threading
import time
try:
    from playsound import playsound
    have_playsound = True
except Exception:
    have_playsound = False

class AlarmApp:
    def __init__(self, root):
        self.root = root
        root.title("Alarm Clock")
        self.alarm_time = None
        self.alarm_thread = None
        self.stop_flag = threading.Event()

        tk.Label(root, text="Set alarm (HH:MM 24-hour):").pack(pady=(10,0))
        self.time_entry = tk.Entry(root, width=10, justify='center')
        self.time_entry.pack(pady=5)
        tk.Label(root, text="Sound file (optional):").pack()
        self.sound_entry = tk.Entry(root, width=30)
        self.sound_entry.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Set Alarm", command=self.set_alarm).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cancel Alarm", command=self.cancel_alarm).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Snooze 5 min", command=self.snooze).pack(side='left', padx=5)

        self.status = tk.Label(root, text="No alarm set", fg="blue")
        self.status.pack(pady=(5,10))

    def alarm_loop(self, alarm_time_str, sound_path):
        while not self.stop_flag.is_set():
            now_str = datetime.now().strftime("%H:%M")
            if now_str == alarm_time_str:
                self._ring(sound_path)
                return
            time.sleep(1)

    def _ring(self, sound_path):
        def ring_actions():
            self.status.config(text=f"Alarm! ({datetime.now().strftime('%H:%M:%S')})", fg="red")
            for i in range(5):
                if self.stop_flag.is_set(): break
                if sound_path and have_playsound:
                    try:
                        playsound(sound_path, block=True)
                    except Exception:
                        print("Could not play file. Using beep.")
                        print('\a')
                else:
                    print('\a')
                time.sleep(2)
            self.status.config(text="No alarm set", fg="blue")
        t = threading.Thread(target=ring_actions, daemon=True)
        t.start()

    def set_alarm(self):
        alarm_time = self.time_entry.get().strip()
        sound = self.sound_entry.get().strip() or None
        try:
            datetime.strptime(alarm_time, "%H:%M")
        except ValueError:
            self.status.config(text="Invalid time format. Use HH:MM", fg="orange")
            return
        self.cancel_alarm()
        self.stop_flag.clear()
        self.alarm_thread = threading.Thread(target=self.alarm_loop, args=(alarm_time, sound), daemon=True)
        self.alarm_thread.start()
        self.alarm_time = alarm_time
        self.status.config(text=f"Alarm set for {alarm_time}", fg="green")

    def cancel_alarm(self):
        self.stop_flag.set()
        self.alarm_time = None
        self.status.config(text="Alarm cancelled", fg="blue")

    def snooze(self, minutes=5):
        if not self.alarm_time:
            self.status.config(text="No active alarm to snooze", fg="orange")
            return
        self.stop_flag.set()
        now = datetime.now() + timedelta(minutes=minutes)
        new_time = now.strftime("%H:%M")
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, new_time)
        self.stop_flag.clear()
        self.set_alarm()
        self.status.config(text=f"Snoozed to {new_time}", fg="green")

if __name__ == "__main__":
    from datetime import timedelta
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
