import tkinter as tk
from tkinter import messagebox, filedialog
import psycopg2
import csv
from data_managment import data_management_gui  # Import the function from the third file

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

# Function to create a new table based on user input and CSV data
def create_table_gui(dbname, user, password, host, port):
    # New window for creating a table
    table_window = tk.Tk()
    table_window.title("Create Table and Import CSV")
    table_window.geometry("500x300")  # Adjusted window size to accommodate tooltips

    # Create and place the labels and entry fields for table creation
    label_table_name = tk.Label(table_window, text="Table Name:")
    label_table_name.grid(row=0, column=0, padx=10, pady=10)

    entry_table_name = tk.Entry(table_window)
    entry_table_name.grid(row=0, column=1, padx=10, pady=10)

    # Add "i" icon and tooltip for Table Name
    info_icon_table_name = tk.Label(table_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_table_name.grid(row=0, column=2, padx=(0, 10))
    Tooltip(info_icon_table_name, "Enter name of table (make it similar to delivrable name).")

    # Function to handle CSV file selection
    def browse_csv():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        entry_csv_path.delete(0, tk.END)
        entry_csv_path.insert(0, file_path)

    label_csv_path = tk.Label(table_window, text="CSV File:")
    label_csv_path.grid(row=1, column=0, padx=10, pady=10)

    entry_csv_path = tk.Entry(table_window)
    entry_csv_path.grid(row=1, column=1, padx=10, pady=10)

    button_browse = tk.Button(table_window, text="Browse", command=browse_csv)
    button_browse.grid(row=1, column=2, padx=10, pady=10)

    # Add "i" icon and tooltip for CSV File
    info_icon_csv = tk.Label(table_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_csv.grid(row=1, column=3, padx=(0, 10))
    Tooltip(info_icon_csv, "Select a CSV file to import data into the table.")

    # Function to create the table and import CSV data
    def create_table_and_import():
        table_name = entry_table_name.get()
        csv_file = entry_csv_path.get()

        if not table_name or not csv_file:
            messagebox.showerror("Error", "Please provide both table name and CSV file.")
            return

        try:
            # Database connection
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            cur = conn.cursor()

            # Create the table (predetermined columns)
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id_troncon TEXT,
                date_viste DATE,
                id TEXT,
                nom_techni TEXT,
                code TEXT,
                id_ch_etiq TEXT,
                cod_gps_x TEXT,
                cod_gps_y TEXT,
                emplac_ch TEXT,
                cmnt_eta_c TEXT,
                type_ch TEXT,
                c_pano_av TEXT,
                pho_fer_av TEXT,
                c_ouv_av_1 TEXT,
                boite24fo TEXT,
                boite72fo TEXT,
                boite144fo TEXT,
                cmt_etat_b TEXT,
                exist_ch TEXT,
                asp_exter TEXT,
                sys_fermet TEXT,
                nett_inter TEXT,
                nett_exter TEXT,
                fix_boite TEXT,
                exis_mou TEXT,
                fix_love_c TEXT,
                tampons_ch TEXT,
                logo TEXT,
                position TEXT,
                etiq_cable TEXT,
                entre2ch TEXT,
                syno TEXT,
                pht_mas_a TEXT,
                pht_mas_b TEXT,
                pht_mas_c TEXT,
                pht_mas_d TEXT,
                act_asp_ex TEXT,
                rep_sy_fer TEXT,
                for_sy_fer TEXT,
                betonnage TEXT,
                act_net_in TEXT,
                act_net_ex TEXT,
                act_fixboi TEXT,
                act_fixlov TEXT,
                act_tampch TEXT,
                act_etiq_c TEXT,
                etiq_chbr TEXT,
                cmnt_actio TEXT,
                ch_fer_apr TEXT,
                c_ouv_ap2 TEXT,
                c_pano_apr TEXT,
                valider TEXT,
                week TEXT
            );
            """
            cur.execute(create_table_query)

            # Open the CSV file and insert data
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                for row in reader:
                    cur.execute(f"""
                    INSERT INTO {table_name}
                    VALUES ({', '.join(['%s'] * len(row))});
                    """, row)
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", f"Table {table_name} created and data imported successfully!")
            table_window.destroy()
            data_management_gui(dbname, user, password, host, port, table_name)  # Close the table creation window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the submit button to create the table and import data
    button_create_table = tk.Button(table_window, text="Create Table and Import CSV", command=create_table_and_import)
    button_create_table.grid(row=2, column=0, columnspan=3, pady=20)

    # Add "i" icon and tooltip for Create Table and Import CSV button
    info_icon_create = tk.Label(table_window, text="ⓘ", fg="blue", cursor="hand2")
    info_icon_create.grid(row=2, column=3, padx=(0, 10))
    Tooltip(info_icon_create, "Click to create the table and import data from the selected CSV file.")

    # Function to close the table creation window
    def close_window():
        table_window.destroy()

    # Close the window when the X icon is clicked
    table_window.protocol("WM_DELETE_WINDOW", close_window)
    table_window.mainloop()