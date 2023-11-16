import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image, ImageTk
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_clipboard():
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            extracted_text = pytesseract.image_to_string(image)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, extracted_text)
        else:
            messagebox.showinfo("No Image", "Clipboard does not contain an image.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def check_clipboard():
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            display_image_on_canvas(image)
    except Exception as e:
        print("Error checking clipboard:", e)
    finally:
        # Check the clipboard again after 1000 milliseconds (1 second)
        root.after(1000, check_clipboard)

def display_image_on_canvas(image):
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor='nw', image=canvas.image)

def clear_text_box():
    text_box.delete('1.0', tk.END)
    canvas.delete("all")

def copy_text_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(text_box.get("1.0", tk.END))

root = tk.Tk()
root.title("OCR from Clipboard")
root.geometry("800x600")  # Set initial size of the window

canvas = tk.Canvas(root, height=300)
canvas.pack(padx=10, pady=10, fill='both', expand=True)

text_box = tk.Text(root, height=10, width=50)
text_box.pack(padx=10, pady=10, fill='both', expand=True)

button_frame = tk.Frame(root)
button_frame.pack(fill='x', expand=False)

extract_button = tk.Button(button_frame, text="Extract Text from Clipboard", command=extract_text_from_clipboard)
extract_button.pack(side='left', padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear Text", command=clear_text_box)
clear_button.pack(side='left', padx=5, pady=5)

copy_button = tk.Button(button_frame, text="Copy Text", command=copy_text_to_clipboard)
copy_button.pack(side='left', padx=5, pady=5)

# Start the periodic clipboard check
check_clipboard()

root.mainloop()
