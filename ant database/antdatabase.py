import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox


class Colony:
    def __init__(self, master):
        self.master = master
        self.master.title("Ant Colony Tracker")

        self.listbox = tk.Listbox(master)
        self.listbox.pack()

        self.new_button = tk.Button(master, text="New Colony", command=self.new_colony)
        self.new_button.pack()

        self.edit_button = tk.Button(master, text="Edit Colony", command=self.edit_colony)
        self.edit_button.pack()

        self.view_button = tk.Button(master, text="View Colony", command=self.view_colony)
        self.view_button.pack()

        self.delete_button = tk.Button(master, text="Delete Colony", command=self.delete_colony)
        self.delete_button.pack()

        self.setup_db()
        self.populate_listbox()

        self.setup_db()
        self.populate_listbox()

    def setup_db(self):
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS colonies
                     (name text PRIMARY KEY, species text, size text, requirements text, 
                     feed_freq integer, water_freq integer, clean_freq integer, last_feed date, 
                     last_water date, last_clean date)''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (colony_name text, action text, date date, message text)''')
        conn.commit()
        conn.close()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM colonies'):
            name = row[0]
            now = datetime.now()
            end_feed_time = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=row[4])
            end_water_time = datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=row[5])
            end_clean_time = datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S.%f') + timedelta(days=row[6])

            if now > end_feed_time:
                name += " - needs feeding"
            if now > end_water_time:
                name += " - needs watering"
            if now > end_clean_time:
                name += " - needs cleaning"
            self.listbox.insert(tk.END, name)
        conn.close()

    def new_colony(self):
        new_window = tk.Toplevel(self.master)
        new_colony = NewColony(new_window, self)

    def edit_colony(self):
        selected_colony = self.listbox.get(self.listbox.curselection())
        # Split the selected colony at the first occurrence of ' -'
        colony_name = selected_colony.split(' -', 1)[0]
        new_window = tk.Toplevel(self.master)
        edit_colony = EditColony(new_window, colony_name, self)
      

    def view_colony(self):
        selected_colony = self.listbox.get(self.listbox.curselection())
        # Split the selected colony at the first occurrence of ' -'
        colony_name = selected_colony.split(' -', 1)[0]
        new_window = tk.Toplevel(self.master)
        view_colony = ViewColony(new_window, colony_name, self)

    def delete_colony(self):
        selected_colony = self.listbox.get(self.listbox.curselection())
        # Split the selected colony at the first occurrence of ' -'
        colony_name = selected_colony.split(' -', 1)[0]
        confirm = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the colony: {colony_name}?")
        if confirm:
            conn = sqlite3.connect('ant_colonies.db')
            c = conn.cursor()
            c.execute('DELETE FROM colonies WHERE name=?', (colony_name,))
            conn.commit()
            conn.close()
            self.populate_listbox()
            
class NewColony:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("New Colony")

        tk.Label(master, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        tk.Label(master, text="Species:").grid(row=1, column=0)
        self.species_entry = tk.Entry(master)
        self.species_entry.grid(row=1, column=1)

        tk.Label(master, text="Size:").grid(row=2, column=0)
        self.size_entry = tk.Entry(master)
        self.size_entry.grid(row=2, column=1)

        tk.Label(master, text="Requirements:").grid(row=3, column=0)
        self.req_entry = tk.Entry(master)
        self.req_entry.grid(row=3, column=1)

        tk.Label(master, text="Feed frequency (days):").grid(row=4, column=0)
        self.feed_freq_entry = tk.Entry(master)
        self.feed_freq_entry.grid(row=4, column=1)

        tk.Label(master, text="Water frequency (days):").grid(row=5, column=0)
        self.water_freq_entry = tk.Entry(master)
        self.water_freq_entry.grid(row=5, column=1)

        tk.Label(master, text="Clean frequency (days):").grid(row=6, column=0)
        self.clean_freq_entry = tk.Entry(master)
        self.clean_freq_entry.grid(row=6, column=1)

        self.save_button = tk.Button(master, text="Save Colony", command=self.save_colony)
        self.save_button.grid(row=7, column=0, columnspan=2)

    def save_colony(self):
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('INSERT INTO colonies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                  (self.name_entry.get(), self.species_entry.get(), self.size_entry.get(), 
                   self.req_entry.get(), float(self.feed_freq_entry.get()), 
                   float(self.water_freq_entry.get()), float(self.clean_freq_entry.get()), 
                   datetime.now(), datetime.now(), datetime.now()))
        conn.commit()
        conn.close()
        self.app.populate_listbox()
        self.master.destroy()

class EditColony:
    def __init__(self, master, colony_name, app):
        self.master = master
        self.colony_name = colony_name
        self.app = app
        self.master.title(f"Edit Colony - {colony_name}")

        tk.Label(master, text="Species:").grid(row=0, column=0)
        self.species_entry = tk.Entry(master)
        self.species_entry.grid(row=0, column=1)

        tk.Label(master, text="Size:").grid(row=1, column=0)
        self.size_entry = tk.Entry(master)
        self.size_entry.grid(row=1, column=1)

        tk.Label(master, text="Requirements:").grid(row=2, column=0)
        self.req_entry = tk.Entry(master)
        self.req_entry.grid(row=2, column=1)

        tk.Label(master, text="Feed frequency (days):").grid(row=3, column=0)
        self.feed_freq_entry = tk.Entry(master)
        self.feed_freq_entry.grid(row=3, column=1)

        tk.Label(master, text="Water frequency (days):").grid(row=4, column=0)
        self.water_freq_entry = tk.Entry(master)
        self.water_freq_entry.grid(row=4, column=1)

        tk.Label(master, text="Clean frequency (days):").grid(row=5, column=0)
        self.clean_freq_entry = tk.Entry(master)
        self.clean_freq_entry.grid(row=5, column=1)

        self.save_button = tk.Button(master, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=6, column=0, columnspan=2)

        self.load_colony()

    def load_colony(self):
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('SELECT * FROM colonies WHERE name=?', (self.colony_name,))
        colony = c.fetchone()
        self.species_entry.insert(0, colony[1])
        self.size_entry.insert(0, colony[2])
        self.req_entry.insert(0, colony[3])
        self.feed_freq_entry.insert(0, str(colony[4]))
        self.water_freq_entry.insert(0, str(colony[5]))
        self.clean_freq_entry.insert(0, str(colony[6]))
        conn.close()

    def save_changes(self):
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('UPDATE colonies SET species=?, size=?, requirements=?, feed_freq=?, water_freq=?, clean_freq=? WHERE name=?', 
            (self.species_entry.get(), self.size_entry.get(), self.req_entry.get(), 
            float(self.feed_freq_entry.get()), 
            float(self.water_freq_entry.get()), 
            float(self.clean_freq_entry.get()), 
            self.colony_name))
        conn.commit()
        conn.close()
        self.app.populate_listbox()
        self.master.destroy()

class LogAction:
    def __init__(self, master, colony_name, action, callback):
        self.master = master
        self.colony_name = colony_name
        self.action = action
        self.callback = callback
        self.master.title(f"Log {action.capitalize()}")

        self.message_entry = tk.Text(master, height=4, width=50)
        self.message_entry.pack()

        self.save_button = tk.Button(master, text=f"Save Log", command=self.save_log)
        self.save_button.pack()

    def save_log(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('INSERT INTO logs VALUES (?, ?, ?, ?)', 
                  (self.colony_name, self.action, datetime.now(), message))
         # after saving the log, update the colony in the database to remove the mention of needing feeding/watering/cleaning
        if self.action == "feed":
            c.execute('UPDATE colonies SET name = replace(name, " - needs feeding", "") WHERE name LIKE ?',
                      (self.colony_name + ' - needs feeding%',))
        elif self.action == "water":
            c.execute('UPDATE colonies SET name = replace(name, " - needs watering", "") WHERE name LIKE ?',
                      (self.colony_name + ' - needs watering%',))
        elif self.action == "clean":
            c.execute('UPDATE colonies SET name = replace(name, " - needs cleaning", "") WHERE name LIKE ?',
                      (self.colony_name + ' - needs cleaning%',))

        conn.commit()
        conn.close()
        self.callback()
        self.master.destroy()

class ViewColony:
    def __init__(self, master, colony_name, app):
        self.master = master
        self.colony_name = colony_name
        self.app = app
        self.master.title("View Colony")
        self.load_colony()

    def load_colony(self):
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        c.execute('SELECT * FROM colonies WHERE name=?', (self.colony_name,))
        colony = c.fetchone()
        conn.close()

        if colony is None:
            messagebox.showerror("Error", f"Colony {self.colony_name} does not exist.")
            return

        self.species_label = tk.Label(self.master, text=f"Species: {colony[1]}")
        self.species_label.pack()

        self.size_label = tk.Label(self.master, text=f"Size: {colony[2]}")
        self.size_label.pack()

        self.requirements_label = tk.Label(self.master, text=f"Requirements: {colony[3]}")
        self.requirements_label.pack()

        next_feed = (datetime.strptime(colony[7],'%Y-%m-%d %H:%M:%S.%f') + timedelta(days=colony[4])).strftime('%Y-%m-%d %H:%M:%S.%f')
        next_water = (datetime.strptime(colony[8],'%Y-%m-%d %H:%M:%S.%f') + timedelta(days=colony[5])).strftime('%Y-%m-%d %H:%M:%S.%f')
        next_clean = (datetime.strptime(colony[9],'%Y-%m-%d %H:%M:%S.%f') + timedelta(days=colony[6])).strftime('%Y-%m-%d %H:%M:%S.%f')

        self.feed_button = tk.Button(self.master, text=f"Log Feed (next feed: {next_feed})", command=self.log_feed)
        self.feed_button.pack()

        self.water_button = tk.Button(self.master, text=f"Log Water (next water: {next_water})", command=self.log_water)
        self.water_button.pack()

        self.clean_button = tk.Button(self.master, text=f"Log Clean (next clean: {next_clean})", command=self.log_clean)
        self.clean_button.pack()

        self.view_logs_button = tk.Button(self.master, text="View Logs", command=self.view_logs)
        self.view_logs_button.pack()

    def load_logs(self):
        self.log_listbox.delete(0, tk.END)
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM logs WHERE colony_name=? ORDER BY date DESC', (self.colony_name,)):
            self.log_listbox.insert(tk.END, f"{row[1].capitalize()} - {row[2]} - {row[3]}")
        conn.close()

    def log_action(self, action, update_field):
        def update_last_action_date():
            conn = sqlite3.connect('ant_colonies.db')
            c = conn.cursor()
            c.execute(f'UPDATE colonies SET {update_field}=? WHERE name=?', (datetime.now(), self.colony_name))
            conn.commit()
            conn.close()
            self.load_colony()
        new_window = tk.Toplevel(self.master)
        log_action = LogAction(new_window, self.colony_name, action, update_last_action_date)

    def log_feed(self):
        self.log_action("feed", "last_feed")

    def log_water(self):
        self.log_action("water", "last_water")

    def log_clean(self):
        self.log_action("clean", "last_clean")

    def view_logs(self):
        new_window = tk.Toplevel(self.master)
        view_logs = ViewLogs(new_window, self.colony_name)


class ViewLogs:
    def __init__(self, master, colony_name):
        self.master = master
        self.colony_name = colony_name
        self.master.title("Logs")

        self.log_listbox = tk.Listbox(master)
        self.log_listbox.pack()
        self.view_button = tk.Button(master, text="View Message", command=self.view_message)
        self.view_button.pack()

        self.load_logs()

    def load_logs(self):
        self.log_listbox.delete(0, tk.END)
        conn = sqlite3.connect('ant_colonies.db')
        c = conn.cursor()
        self.logs = c.execute('SELECT * FROM logs WHERE colony_name=? ORDER BY date DESC', (self.colony_name,)).fetchall()
        for log in self.logs:
            self.log_listbox.insert(tk.END, f"{log[1].capitalize()} - {log[2]}")
        conn.close()

    def view_message(self):
        selected_log_index = self.log_listbox.curselection()[0]
        selected_log = self.logs[selected_log_index]
        new_window = tk.Toplevel(self.master)
        view_log_message = ViewLogMessage(new_window, selected_log)


class ViewLogMessage:
    def __init__(self, master, log):
        self.master = master
        self.master.title(f"Message - {log[1].capitalize()} - {log[2]}")

        self.message_text = tk.Text(master, height=10, width=50)
        self.message_text.insert(tk.END, log[3])
        self.message_text.pack()


if __name__ == "__main__":
    root = tk.Tk()
    gui = Colony(root)
    root.mainloop()
