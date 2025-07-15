import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif
import pillow_heif

pillow_heif.register_heif_opener()

def remove_exif(image_path):
    """
    Removes EXIF data from a single image file.
    """
    try:
        img = Image.open(image_path)
        img.info.pop('exif', None)
        
        save_options = {'format': img.format}
        if img.format == 'JPEG':
            save_options['quality'] = 'keep'
        elif img.format == 'HEIF':
            save_options['quality'] = -1  # lossless for heif

        img.save(image_path, **save_options)
        return True, f"Successfully removed EXIF data from {image_path}"
    except FileNotFoundError:
        return False, f"Error: The file was not found at {image_path}"
    except Exception as e:
        return False, f"An error occurred while processing {image_path}: {e}"

def select_files_and_remove_exif():
    """
    Opens a file dialog to select multiple image files and removes EXIF data from them.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_paths = filedialog.askopenfilenames(
        title="Select one or more images",
        filetypes=[
            ("All supported images", "*.jpg *.jpeg *.png *.tiff *.bmp *.gif *.heic *.heif"),
            ("HEIC/HEIF", "*.heic *.heif"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("TIFF", "*.tiff"),
            ("Bitmap", "*.bmp"),
            ("GIF", "*.gif"),
            ("All files", "*.*")
        ]
    )

    if not file_paths:
        messagebox.showinfo("No files selected", "No image files were selected.")
        return

    success_count = 0
    error_messages = []

    for file_path in file_paths:
        success, message = remove_exif(file_path)
        if success:
            success_count += 1
        else:
            error_messages.append(message)

    if success_count > 0:
        messagebox.showinfo("Success", f"Successfully removed EXIF data from {success_count} image(s).")

    if error_messages:
        messagebox.showerror("Errors Occurred", "\n".join(error_messages))

if __name__ == "__main__":
    select_files_and_remove_exif()