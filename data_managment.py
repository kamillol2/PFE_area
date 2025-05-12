import psycopg2
import tkinter as tk
from quick_report import main
from data_testing_final import main as data_fixing_main
from full_report import main as full_report_main
import csv
from tkinter import filedialog, messagebox

# Tooltip class for adding hover-based tooltips
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Function to export data as CSV
def export_data_as_csv(dbname, user, password, host, port, table_name):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_path:
            return  # User canceled the save dialog

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(rows)

        messagebox.showinfo("Success", f"Data exported to {file_path}")
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Function to create the data management GUI
def data_management_gui(dbname, user, password, host, port, selected_table):
    data_window = tk.Tk()
    data_window.title("Data Management")
    data_window.geometry("500x400")  # Adjusted window size to accommodate tooltips

    # Create and place the buttons
    button_gathering = tk.Button(data_window, text="Quick Report", command=lambda: main(dbname, user, password, host, port, selected_table), width=20, height=2)
    button_gathering.pack(pady=10)

    # Add "i" icon and tooltip for Quick Report button
    info_icon_gathering = tk.Label(data_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_gathering.pack()
    Tooltip(info_icon_gathering, "Quick information on quality of data (if all 0 data is clean of mistakes) .")

    button_formatting = tk.Button(data_window, text="Data FIX / TEST", command=lambda: data_fixing_main(dbname, user, password, host, port, selected_table), width=20, height=2)
    button_formatting.pack(pady=10)

    # Add "i" icon and tooltip for Data FIX / TEST button
    info_icon_formatting = tk.Label(data_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_formatting.pack()
    Tooltip(info_icon_formatting, "Fix/test/report on the data in the selected table.")

    button_fixing = tk.Button(data_window, text="Full Report", command=lambda: full_report_main(dbname, user, password, host, port, selected_table), width=20, height=2)
    button_fixing.pack(pady=10)

    # Add "i" icon and tooltip for Full Report button
    info_icon_fixing = tk.Label(data_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_fixing.pack()
    Tooltip(info_icon_fixing, "full report with ID's of missing/unfound files with detailed statitics .")

    button_export_csv = tk.Button(data_window, text="Export Data as CSV", command=lambda: export_data_as_csv(dbname, user, password, host, port, selected_table), width=20, height=2)
    button_export_csv.pack(pady=10)

    # Add "i" icon and tooltip for Export Data as CSV button
    info_icon_export = tk.Label(data_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_export.pack()
    Tooltip(info_icon_export, "Export the data from the selected table as a CSV file (for QGIS).")

    # Function to close the window
    def close_window():
        data_window.destroy()

    # Close the window when the X icon is clicked
    data_window.protocol("WM_DELETE_WINDOW", close_window)

    # Run the GUI
    data_window.mainloop()

# Run the data management GUI when this file is executed
if __name__ == "__main__":
    data_management_gui()