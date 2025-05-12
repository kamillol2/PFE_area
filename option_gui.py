import tkinter as tk
from table_creation import create_table_gui
from selection_gui import select_existing_table

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

# Function to create the main GUI after login
def choice_gui(dbname, user, password, host, port):
    # Create the main window
    main_window = tk.Tk()
    main_window.title("Table Selection")
    main_window.geometry("400x300")  # Increased size to accommodate tooltips

    # Create and place the buttons
    button_create_table = tk.Button(main_window, text="Create New Table", command=lambda: create_table_gui(dbname, user, password, host, port), width=20, height=2)
    button_create_table.pack(pady=10)

    # Add "i" icon and tooltip for Create New Table button
    info_icon_create = tk.Label(main_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_create.pack()
    Tooltip(info_icon_create, "If you have a new delivrable, click here to create a new table.")

    button_select_table = tk.Button(main_window, text="Select Existing Table", command=lambda: select_existing_table(dbname, user, password, host, port), width=20, height=2)
    button_select_table.pack(pady=10)

    # Add "i" icon and tooltip for Select Existing Table button
    info_icon_select = tk.Label(main_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_select.pack()
    Tooltip(info_icon_select, "Click to select an existing table to check on past treated delivrables.")

    def close_window():
        main_window.destroy()
        exit()

    main_window.protocol("WM_DELETE_WINDOW", close_window)

    # Run the main window
    main_window.mainloop()