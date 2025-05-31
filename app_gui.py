# app_gui.py
# This file handles the Graphical User Interface for the Morse Code Converter.

import tkinter as tk
from tkinter import ttk, messagebox
import Morse_Code_Intrepreter # Import your core logic file

class MorseConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Converter")
        self.root.geometry("600x550") # Set a default window size
        self.root.resizable(True, True) # Allow resizing

        # Configure styling for a more modern look
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.configure('TLabel', font=('Arial', 11), background='#e0e0e0')
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TText', font=('Consolas', 11))

        self.create_widgets()

    def create_widgets(self):
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="10 10 10 10")
        input_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.input_label = ttk.Label(input_frame, text="Enter Text or Morse Code:")
        self.input_label.pack(pady=(0, 5), anchor="w")

        # Text widget for multi-line input
        self.input_text = tk.Text(input_frame, height=8, width=50, wrap="word", font=('Consolas', 11))
        self.input_text.pack(fill="both", expand=True)

        # --- Buttons Frame ---
        button_frame = ttk.Frame(self.root, padding="10 0 10 0")
        button_frame.pack(pady=5)

        self.text_to_morse_btn = ttk.Button(button_frame, text="Convert Text to Morse", command=self.convert_text_to_morse)
        self.text_to_morse_btn.grid(row=0, column=0, padx=5, pady=5)

        self.morse_to_text_btn = ttk.Button(button_frame, text="Convert Morse to Text", command=self.convert_morse_to_text)
        self.morse_to_text_btn.grid(row=0, column=1, padx=5, pady=5)

        self.save_btn = ttk.Button(button_frame, text="Save Conversion", command=self.save_current_conversion)
        self.save_btn.grid(row=0, column=2, padx=5, pady=5)

        # --- Output Frame ---
        output_frame = ttk.LabelFrame(self.root, text="Output", padding="10 10 10 10")
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_label = ttk.Label(output_frame, text="Converted Result:")
        self.output_label.pack(pady=(0, 5), anchor="w")

        # Text widget for multi-line output (read-only)
        self.output_text = tk.Text(output_frame, height=8, width=50, wrap="word", state='disabled', font=('Consolas', 11))
        self.output_text.pack(fill="both", expand=True)

        # --- Status Message Label ---
        self.status_label = ttk.Label(self.root, text="", foreground="blue", font=('Arial', 10, 'italic'))
        self.status_label.pack(pady=(0, 10))

        # Store last conversion for saving
        self.last_original_input = ""
        self.last_converted_output = ""
        self.last_conversion_type = ""

    def update_output(self, text, message="", color="blue"):
        """Helper to update output Text widget and status label."""
        self.output_text.config(state='normal') # Enable editing temporarily
        self.output_text.delete(1.0, tk.END) # Clear previous content
        self.output_text.insert(tk.END, text) # Insert new text
        self.output_text.config(state='disabled') # Make it read-only again

        self.status_label.config(text=message, foreground=color)

    def convert_text_to_morse(self):
        input_str = self.input_text.get(1.0, tk.END).strip()
        converted_morse, success, warning = Morse_Code_Intrepreter.text_to_morse(input_str)

        if success:
            self.last_original_input = input_str
            self.last_converted_output = converted_morse
            self.last_conversion_type = "text_to_morse"
            message = "Conversion successful!"
            if warning:
                message += f"\n{warning}"
                self.update_output(converted_morse, message, color="orange")
            else:
                self.update_output(converted_morse, message, color="green")
        else:
            self.update_output("", converted_morse, color="red") # Display error in status

    def convert_morse_to_text(self):
        input_str = self.input_text.get(1.0, tk.END).strip()
        converted_text, success, warning = Morse_Code_Intrepreter.morse_to_text(input_str)

        if success:
            self.last_original_input = input_str
            self.last_converted_output = converted_text
            self.last_conversion_type = "morse_to_text"
            message = "Conversion successful!"
            if warning:
                message += f"\n{warning}"
                self.update_output(converted_text, message, color="orange")
            else:
                self.update_output(converted_text, message, color="green")
        else:
            self.update_output("", converted_text, color="red") # Display error in status

    def save_current_conversion(self):
        if not self.last_converted_output:
            messagebox.showwarning("No Conversion", "Please perform a conversion first before saving.")
            return

        success, message = Morse_Code_Intrepreter.save_conversion(
            self.last_original_input,
            self.last_converted_output,
            self.last_conversion_type
        )
        if success:
            messagebox.showinfo("Save Successful", message)
            self.status_label.config(text=message, foreground="green")
        else:
            messagebox.showerror("Save Error", message)
            self.status_label.config(text=message, foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = MorseConverterApp(root)
    root.mainloop()