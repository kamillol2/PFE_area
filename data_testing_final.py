import psycopg2
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from test_new_freport import main as full_report_gui

# List of columns to check for data fixing
columns_to_check = [
    "c_pano_av", "syno", "pht_mas_a", "pht_mas_b", "pht_mas_c", "pht_mas_d",
    "ch_fer_apr", "c_ouv_ap2", "c_pano_apr", "pho_fer_av", "c_ouv_av_1"
]

# SQL queries for data fixing (optimized)
SQL_FIXING_QUERIES = [
    r"""
    -- Standardize NULL and empty values
    UPDATE {table} SET {col} = 'Link Not Found' WHERE {col} IS NULL OR {col} = '';
    """,
    r"""
    -- Remove double extensions and replace invalid ones with .jpg
    UPDATE {table} SET {col} = REGEXP_REPLACE({col}, '\.[a-zA-Z0-9]+$', '')
    WHERE {col} ~* '\.(jpg|jpeg|png|gif|heic|tiff|bmp)\.\1$';
    """,
    r"""
    -- Ensure .jpeg extension for QField images
    UPDATE {table} SET {col} = {col} || '.jpeg' WHERE {col} NOT ILIKE '%.%' AND {col} ILIKE '%qfield%';
    """,
    r"""
    -- Ensure .jpg extension for all images
    UPDATE {table} SET {col} = REGEXP_REPLACE({col}, '\.[a-zA-Z0-9]+$', '.jpg')
    WHERE {col} NOT ILIKE '%.jpg' AND {col} NOT ILIKE '%.jpeg';
    """,
    r"""
    -- Standardize file paths (adding slashes and renaming directories)
    UPDATE {table} SET {col} =
        CASE
            WHEN {col} ILIKE 'files%' AND NOT {col} ILIKE 'files/%' THEN 'files/' || {col}
            WHEN {col} ILIKE 'DCIM%' AND NOT {col} ILIKE 'DCIM/%' THEN 'DCIM/' || {col}
            WHEN {col} ILIKE 'files/%' THEN REPLACE({col}, 'files/', 'DCIM/')
            ELSE {col}
        END;
    """
]

def execute_fixing_queries(conn, table_name, progress_callback=None):
    try:
        with conn.cursor() as cursor:
            total_steps = len(columns_to_check) * len(SQL_FIXING_QUERIES)
            current_step = 0
            total_updates = 0
            
            for column in columns_to_check:
                for query in SQL_FIXING_QUERIES:
                    # Format the query with the column and table name
                    formatted_query = query.format(col=column, table=table_name)
                    
                    # Execute the formatted query
                    cursor.execute(formatted_query)
                    total_updates += cursor.rowcount
                    current_step += 1
                    if progress_callback:
                        progress_callback((current_step / total_steps) * 100)
            
            conn.commit()
        return total_updates
    except Exception as e:
        conn.rollback()
        raise e


def check_file_existence(conn, table_name, folder_path, progress_callback=None):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_rows = cursor.fetchone()[0] * len(columns_to_check)
            processed_rows, total_updates = 0, 0
            
            for column in columns_to_check:
                cursor.execute(f"""
                    SELECT {column}
                    FROM {table_name};
                """)
                rows = cursor.fetchall()
                
                for row in rows:
                    file_path = row[0]
                    processed_rows += 1
                    if not file_path or file_path.startswith(('Link Not Found', 'File Not Found')):
                        continue
                    
                    # Fix for paths that include DCIM/ prefix
                    actual_path = file_path
                    if file_path.startswith('DCIM/'):
                        # If the selected folder ends with DCIM, don't add it again
                        if folder_path.endswith('DCIM'):
                            # Strip 'DCIM/' from the beginning and join with folder path
                            actual_path = os.path.join(folder_path, file_path[5:])
                        else:
                            # Use the path as is
                            actual_path = os.path.join(folder_path, file_path)
                    else:
                        # For paths without DCIM prefix, use as is
                        actual_path = os.path.join(folder_path, file_path)
                    
                    if not os.path.isfile(actual_path):
                        cursor.execute(
                            f"UPDATE {table_name} SET {column} = %s WHERE {column} = %s",
                            ('File Not Found', file_path)
                        )
                        total_updates += cursor.rowcount
                    
                    if progress_callback and processed_rows % 50 == 0:
                        progress_callback((processed_rows / total_rows) * 100)
            
            conn.commit()
            return total_updates
    except Exception as e:
        conn.rollback()
        raise e

class EnhancedDataFixingDialog:
    def __init__(self, parent, dbname, user, password, host, port, table_name):
        self.parent = parent
        self.db_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.table_name = table_name
        self.folder_path = None
        
        # Create a new top-level window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Enhanced Data Fixing Tool")
        self.dialog.geometry("800x600")
        
        # Make the dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)  # Reduced padding
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Database Image Path Fixing Tool", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))  # Reduced padding
        
        # Folder selection frame
        folder_frame = tk.LabelFrame(main_frame, text="Image Folder Selection", padx=10, pady=10)  # Reduced padding
        folder_frame.pack(fill=tk.X, pady=(5, 10))  # Reduced padding
        
        # Folder path display with horizontal scrolling
        path_frame = tk.Frame(folder_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        # Add horizontal scrollbar for path entry
        path_scroll = tk.Scrollbar(path_frame, orient='horizontal')
        path_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.path_var = tk.StringVar()
        self.path_var.set("No folder selected")
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, 
                            state='readonly', xscrollcommand=path_scroll.set)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        path_scroll.config(command=path_entry.xview)
        
        browse_button = tk.Button(path_frame, text="Browse...", command=self.browse_folder)
        browse_button.pack(side=tk.RIGHT)
        
        # Options frame
        options_frame = tk.LabelFrame(main_frame, text="Operation Options", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Checkboxes for operations
        self.fix_paths_var = tk.BooleanVar(value=True)
        fix_paths_cb = tk.Checkbutton(options_frame, text="Fix path formatting issues", 
                                      variable=self.fix_paths_var)
        fix_paths_cb.pack(anchor=tk.W, pady=2)
        
        self.check_existence_var = tk.BooleanVar(value=True)
        check_existence_cb = tk.Checkbutton(options_frame, text="Check file existence", 
                                           variable=self.check_existence_var)
        check_existence_cb.pack(anchor=tk.W, pady=2)
        
        self.launch_report_var = tk.BooleanVar(value=True)
        launch_report_cb = tk.Checkbutton(options_frame, text="Launch full report after completion", 
                                         variable=self.launch_report_var)
        launch_report_cb.pack(anchor=tk.W, pady=2)
        
        # Status and progress frame
        status_frame = tk.LabelFrame(main_frame, text="Status", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start")
        status_label = tk.Label(status_frame, textvariable=self.status_var, anchor="w")
        status_label.pack(fill=tk.X)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 0))
        
        self.start_button = tk.Button(button_frame, text="Start", command=self.run_data_fixing, 
                                     width=10)
        self.start_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, 
                                 width=10)
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Update initial window size
        self.dialog.geometry("600x500")  # Set fixed initial size
        self.dialog.minsize(500, 400)    # Set minimum size
    
    def browse_folder(self):
        """Open a file dialog to select the DCIM folder"""
        folder_selected = filedialog.askdirectory(title="Select Folder Containing Image Files")
        if folder_selected:
            self.folder_path = folder_selected
            self.path_var.set(folder_selected)
    
    def update_progress(self, value, message):
        """Update the progress bar and status message"""
        self.progress_var.set(value)
        self.status_var.set(message)
        self.dialog.update_idletasks()
    
    def run_data_fixing(self):
        """Execute the selected data fixing operations"""
        # Check if folder is required and selected
        if self.check_existence_var.get() and not self.folder_path:
            messagebox.showwarning("Warning", "Please select a folder for file existence check.")
            return
        
        # Disable the start button to prevent multiple executions
        self.start_button.config(state=tk.DISABLED)
        
        try:
            # Log the start of operations
            self.update_progress(0, "Starting operations...")
            
            # Initialize counters
            fixing_updates = 0
            existence_updates = 0
            
            # Connect to the database
            try:
                conn = psycopg2.connect(**self.db_params)
            except Exception as db_error:
                raise Exception(f"Failed to connect to database: {str(db_error)}")
            
            # Execute path fixing if selected
            if self.fix_paths_var.get():
                self.update_progress(10, "Fixing path formats...")
                
                # Create a progress callback that only uses the percentage
                def fixing_progress(percent):
                    self.update_progress(10 + percent * 0.4, "Fixing path formats...")
                
                fixing_updates = execute_fixing_queries(
                    conn, 
                    self.table_name, 
                    fixing_progress
                )
                
                self.update_progress(50, f"Path fixing completed: {fixing_updates} updates")
            
            # Check file existence if selected
            if self.check_existence_var.get():
                self.update_progress(50, "Checking file existence...")
                
                # Create a progress callback that only uses the percentage
                def existence_progress(percent):
                    self.update_progress(50 + percent * 0.4, "Checking file existence...")
                
                existence_updates = check_file_existence(
                    conn, 
                    self.table_name, 
                    self.folder_path,
                    existence_progress
                )
                
                self.update_progress(90, f"File check completed: {existence_updates} missing files")
            
            # Close the database connection
            conn.close()            
            # Complete the progress bar
            self.update_progress(100, "All operations completed successfully!")
            
            # Show success message
            messagebox.showinfo(
                "Operation Complete", 
                f"Data fixing operations completed successfully!\n\n"
                f"- Format fixing updates: {fixing_updates}\n"
                f"- Missing file updates: {existence_updates}\n"
                f"- Total updates: {fixing_updates + existence_updates}\n\n"
            )
            
            # Launch the full report GUI if selected
            if self.launch_report_var.get():
                self.dialog.destroy()
                
                full_report_gui(
                    self.db_params['dbname'], 
                    self.db_params['user'], 
                    self.db_params['password'], 
                    self.db_params['host'], 
                    self.db_params['port'], 
                    self.table_name,
                    folder_path=self.folder_path
                )
            
        except Exception as e:
            # Show error message
            messagebox.showerror(
                "Error", 
                f"An error occurred during the operation:\n\n{str(e)}\n\n"
            )
            
            # Update status
            self.update_progress(0, f"Operation failed: {str(e)}")
        
        finally:
            # Re-enable the start button
            if self.start_button.winfo_exists():
                self.start_button.config(state=tk.NORMAL)

def main(dbname, user, password, host, port, table_name):
    try:
        root = tk.Tk()
        EnhancedDataFixingDialog(root, dbname, user, password, host, port, table_name)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"Unexpected error:\n\n{str(e)}")
        if 'root' in locals():
            root.destroy()

if __name__ == "__main__":

    main()
