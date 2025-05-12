import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from option_gui import choice_gui  # Import the functions from the selection file

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

# Function to test the connection
def test_connection():
    dbname = entry_dbname.get()
    user = entry_user.get()
    password = entry_password.get()
    host = entry_host.get()
    port = entry_port.get()

    try:
        # Try connecting to the database with the entered credentials
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.close()
        messagebox.showinfo("Success", "Connection successful!")
        root.withdraw()  # Hide the first window
        choice_gui(dbname, user, password, host, port)  # Pass credentials to the next GUI
    except Exception as e:
        messagebox.showerror("Error", f"Connection failed: {e}")

# Create the first window for database login
root = tk.Tk()
root.title("Database Login")

# Create and place the labels and entry fields
label_dbname = tk.Label(root, text="Database Name:")
label_dbname.grid(row=0, column=0, padx=10, pady=10)

entry_dbname = tk.Entry(root)
entry_dbname.grid(row=0, column=1, padx=10, pady=10)

# Add "i" icon and tooltip for Database Name
info_icon_dbname = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_dbname.grid(row=0, column=2, padx=(0, 10))
Tooltip(info_icon_dbname, "Default (postgres)")

label_user = tk.Label(root, text="Username:")
label_user.grid(row=1, column=0, padx=10, pady=10)

entry_user = tk.Entry(root)
entry_user.grid(row=1, column=1, padx=10, pady=10)

# Add "i" icon and tooltip for Username
info_icon_user = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_user.grid(row=1, column=2, padx=(0, 10))
Tooltip(info_icon_user, "Default (postgres)")

label_password = tk.Label(root, text="Password:")
label_password.grid(row=2, column=0, padx=10, pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=10)

# Add "i" icon and tooltip for Password
info_icon_password = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_password.grid(row=2, column=2, padx=(0, 10))
Tooltip(info_icon_password, "Default (postgres) if tutorial followed.")

label_host = tk.Label(root, text="Host:")
label_host.grid(row=3, column=0, padx=10, pady=10)

entry_host = tk.Entry(root)
entry_host.grid(row=3, column=1, padx=10, pady=10)

# Add "i" icon and tooltip for Host
info_icon_host = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_host.grid(row=3, column=2, padx=(0, 10))
Tooltip(info_icon_host, "Default (localhost)")

label_port = tk.Label(root, text="Port:")
label_port.grid(row=4, column=0, padx=10, pady=10)

entry_port = tk.Entry(root)
entry_port.grid(row=4, column=1, padx=10, pady=10)

# Add "i" icon and tooltip for Port
info_icon_port = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_port.grid(row=4, column=2, padx=(0, 10))
Tooltip(info_icon_port, "Default (5432)")

# Create a button to test the connection
test_button = tk.Button(root, text="Test Connection", command=test_connection)
test_button.grid(row=5, column=0, columnspan=2, pady=20)

# Add "i" icon and tooltip for Test Connection button
info_icon_test = tk.Label(root, text="ⓘ", fg="blue", cursor="hand2")
info_icon_test.grid(row=5, column=2, padx=(0, 10))
Tooltip(info_icon_test, "Click to test connection with provided credentials.")

# Close the application when the window is closed
root.protocol("WM_DELETE_WINDOW", root.destroy)

# Run the application
root.mainloop()