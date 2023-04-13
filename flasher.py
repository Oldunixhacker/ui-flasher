# Import the modules
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Define the flash function
def flash():
    # Hide the main window
    window.withdraw()
    # Create a progress window
    progress = tk.Toplevel()
    progress.title("Progress")
    progress.geometry("400x200")
    # Create a progress label
    progress_label = ttk.Label(progress, text="Starting...")
    progress_label.pack(padx=10, pady=10)
    # Create a cancel button
    cancel_button = ttk.Button(progress, text="Cancel", command=lambda: progress.destroy())
    cancel_button.pack(padx=10, pady=10)
    # Create a log text widget
    log_text = tk.Text(progress, state="disabled")
    log_text.pack(padx=10, pady=10)
    # Create a show log checkbox variable
    show_log_var = tk.IntVar()
    # Create a show log checkbox
    show_log_check = ttk.Checkbutton(progress, text="Show logs", variable=show_log_var)
    show_log_check.pack(padx=10, pady=10)
    # Update the progress label
    progress_label.config(text="Getting the selected file path...")
    # Get the selected file path
    file_path = file_entry.get()
    # Check if the file is a valid img file
    if file_path.endswith(".img"):
        # Confirm the flashing operation
        confirm = messagebox.askyesno("Flash", "Are you sure you want to flash this file?")
        if confirm:
            # Get the restore checkbox value
            restore = restore_var.get()
            if restore:
                # Update the progress label
                progress_label.config(text="Getting the backup folder path...")
                # Get the backup folder path
                folder_path = folder_entry.get()
                # Check if the folder path is valid
                if os.path.isdir(folder_path):
                    # Update the progress label
                    progress_label.config(text="Backing up user apps and profile data...")
                    # Disable the cancel button
                    cancel_button.config(state="disabled")
                    # Run the adb command to backup only user apps and profile data to the folder and save the output to a log file
                    os.system(f"adb backup -apk -shared -all -f {folder_path}/backup.ab -system no > backup.log 2>&1")
                    # Show a success message
                    messagebox.showinfo("Backup", "Backup completed successfully.")
                    # Enable the cancel button
                    cancel_button.config(state="normal")
                    # Check if the user wants to see the logs
                    show_log = show_log_var.get()
                    if show_log:
                        # Enable the log text widget and insert the log file content
                        log_text.config(state="normal")
                        with open("backup.log") as f:
                            log_text.insert("end", f.read())
                        log_text.config(state="disabled")
                else:
                    # Show an error message
                    messagebox.showerror("Backup", "Please select a valid folder.")
            # Get the Magisk checkbox value
            magisk = magisk_var.get()
            if magisk:
                # Update the progress label
                progress_label.config(text="Patching the system image with Magisk...")
                # Run the adb commands to patch the system image with Magisk and save the output to a log file
                os.system("adb push magisk.apk /data/local/tmp > magisk.log 2>&1")
                os.system(f"adb shell magisk --install-module {file_path} >> magisk.log 2>&1")
                os.system("adb pull /data/local/tmp/magisk.img >> magisk.log 2>&1")
                os.system("mv magisk.img patched.img >> magisk.log 2>&1")
                # Update the progress label
                progress_label.config(text="Flashing the patched image...")
                # Run the adb commands to flash the patched image and save the output to a log file
                os.system("adb reboot bootloader >> magisk.log 2>&1")
                os.system("fastboot flash update patched.img >> magisk.log 2>&1")
                os.system("fastboot reboot >> magisk.log 2>&1")
            else:
                # Update the progress label
                progress_label.config(text="Flashing the original image...")
                # Run the adb commands to flash the original image and save the output to a log file
                os.system("adb reboot bootloader > flash.log 2>&1")
