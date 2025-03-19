import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
import json

class EnhancedImageResizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Image Resizer")
        self.root.resizable(True, True)
        
        # Configure column and row weights for proper resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        
        # String variables for dynamic text in the GUI
        self.original_dims_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.new_filename_var = tk.StringVar()
        self.selected_folder_var = tk.StringVar()
        self.format_var = tk.StringVar(value="Same as input")
        self.quality_var = tk.IntVar(value=85)
        self.aspect_lock = tk.BooleanVar(value=True)
        
        # Global variables
        self.selected_file = None
        self.original_image = None
        self.preview_photo = None
        self.aspect_ratio = 1.0
        self.width_trace_id = None
        self.height_trace_id = None
        
        # Load config if exists
        self.load_config()
        
        # Create the main frames
        self.create_frames()
        
        # Create all widgets
        self.create_widgets()
        
        # Set up keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Initialize
        self.original_dims_var.set("Original dimensions: ")
        self.status_var.set("Ready to resize images")
        if not self.selected_folder_var.get():
            self.selected_folder_var.set("No folder selected")
    
    def load_config(self):
        """Load saved configuration if available"""
        config_file = "image_resizer_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    folder = config.get("last_folder", "")
                    if folder and os.path.exists(folder):
                        self.selected_folder_var.set(folder)
            except Exception:
                pass
    
    def save_config(self):
        """Save configuration for future use"""
        config_file = "image_resizer_config.json"
        folder = self.selected_folder_var.get()
        if folder and folder != "No folder selected":
            try:
                with open(config_file, "w") as f:
                    json.dump({"last_folder": folder}, f)
            except Exception:
                pass
    
    def create_frames(self):
        """Create the main organizational frames"""
        self.input_frame = ttk.LabelFrame(self.root, text="Input Image")
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.preview_frame = ttk.LabelFrame(self.root, text="Image Preview")
        self.preview_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="nsew")
        
        self.settings_frame = ttk.LabelFrame(self.root, text="Resize Settings")
        self.settings_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.output_frame = ttk.LabelFrame(self.root, text="Output Settings")
        self.output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.action_frame = ttk.Frame(self.root)
        self.action_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    
    def create_widgets(self):
        """Create all widgets for the application"""
        # Input Frame Widgets
        self.browse_button = ttk.Button(self.input_frame, text="Browse Image", command=self.browse_image)
        self.browse_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.original_dims_label = ttk.Label(self.input_frame, textvariable=self.original_dims_var)
        self.original_dims_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Preview Frame Widgets
        self.preview_label = ttk.Label(self.preview_frame, text="No image selected")
        self.preview_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Settings Frame Widgets
        ttk.Label(self.settings_frame, text="New width (pixels):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.width_entry = ttk.Entry(self.settings_frame, textvariable=self.width_var)
        self.width_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.settings_frame, text="New height (pixels):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.height_entry = ttk.Entry(self.settings_frame, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.lock_check = ttk.Checkbutton(self.settings_frame, text="Maintain aspect ratio", variable=self.aspect_lock)
        self.lock_check.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        ttk.Label(self.settings_frame, text="Format:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.format_menu = ttk.OptionMenu(self.settings_frame, self.format_var, "Same as input", "JPG", "PNG", "BMP", "GIF")
        self.format_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.settings_frame, text="JPG Quality:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.quality_slider = ttk.Scale(self.settings_frame, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.quality_var)
        self.quality_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.settings_frame, text="Preset Sizes:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.preset_var = tk.StringVar()
        presets = ["Custom", "Thumbnail (100x100)", "Small (320x240)", "Medium (640x480)", "HD (1280x720)", "Full HD (1920x1080)"]
        self.preset_menu = ttk.OptionMenu(self.settings_frame, self.preset_var, presets[0], *presets, command=self.set_preset_size)
        self.preset_menu.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        # Output Frame Widgets
        ttk.Label(self.output_frame, text="New filename:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.new_filename_entry = ttk.Entry(self.output_frame, textvariable=self.new_filename_var)
        self.new_filename_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.choose_destination_button = ttk.Button(self.output_frame, text="Choose Destination Folder", command=self.choose_destination)
        self.choose_destination_button.grid(row=1, column=0, padx=10, pady=5)
        
        self.selected_folder_label = ttk.Label(self.output_frame, textvariable=self.selected_folder_var, wraplength=300)
        self.selected_folder_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Action Frame Widgets
        self.resize_button = ttk.Button(self.action_frame, text="Resize and Save", command=self.start_resize_thread, state=tk.DISABLED)
        self.resize_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.progress = ttk.Progressbar(self.action_frame, mode="indeterminate", length=400)
        self.progress.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Status Frame Widgets - Replaced Label with Text for log
        self.status_text = tk.Text(self.status_frame, height=3, width=50, state="disabled")
        self.status_text.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.status_text.tag_config("success", foreground="green")
        self.status_text.tag_config("error", foreground="red")
        self.status_text.tag_config("info", foreground="black")
        
        # Set up trace for width/height to maintain aspect ratio
        self.width_trace_id = self.width_var.trace_add("write", self.update_height_from_width)
        self.height_trace_id = self.height_var.trace_add("write", self.update_width_from_height)
    
    def setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts for common operations"""
        self.root.bind("<Control-o>", lambda e: self.browse_image())
        self.root.bind("<Control-s>", lambda e: self.start_resize_thread() if self.resize_button.cget("state") == tk.NORMAL else None)
        self.root.bind("<Control-d>", lambda e: self.choose_destination())
    
    def browse_image(self):
        """Handle the image selection process."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.selected_file = file_path
                
                self.aspect_ratio = self.original_image.width / self.original_image.height
                
                self.original_dims_var.set(f"Original dimensions: {self.original_image.width} x {self.original_image.height}")
                
                base, ext = os.path.splitext(os.path.basename(file_path))
                default_name = base + "_resized" + ext
                self.new_filename_var.set(default_name)
                
                self.resize_button.config(state=tk.NORMAL)
                
                self.width_var.set(str(self.original_image.width))
                self.height_var.set(str(self.original_image.height))
                
                self.update_preview()
                
                self.update_status("Image selected successfully", "success")
            except Exception as e:
                self.update_status(f"Invalid image file: {str(e)}", "error")
                messagebox.showerror("Error", "Invalid image file")
        else:
            self.update_status("No file selected", "info")
    
    def choose_destination(self):
        """Handle the destination folder selection process."""
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder_var.set(folder)
            self.save_config()
        else:
            self.update_status("No folder selected", "info")
    
    def set_preset_size(self, selection):
        """Set dimensions based on preset selection"""
        if selection == "Custom":
            return
        
        sizes = {
            "Thumbnail (100x100)": (100, 100),
            "Small (320x240)": (320, 240),
            "Medium (640x480)": (640, 480),
            "HD (1280x720)": (1280, 720),
            "Full HD (1920x1080)": (1920, 1080)
        }
        
        width, height = sizes.get(selection, (0, 0))
        
        if width > 0 and height > 0:
            self.width_var.set(str(width))
            if not self.aspect_lock.get():
                self.height_var.set(str(height))
    
    def update_preview(self):
        """Update the preview image in the GUI"""
        if not self.selected_file or not self.original_image:
            self.preview_label.config(text="No image selected", image="")
            return
        
        preview_image = self.original_image.copy()
        preview_image.thumbnail((300, 300))
        self.preview_photo = ImageTk.PhotoImage(preview_image)
        self.preview_label.config(image=self.preview_photo)
    
    def update_height_from_width(self, *args):
        """Update height based on width to maintain aspect ratio"""
        if not self.aspect_lock.get() or not self.selected_file:
            return
        
        try:
            width = int(self.width_var.get())
            new_height = int(round(width / self.aspect_ratio))
            
            if self.height_trace_id:
                self.height_var.trace_remove("write", self.height_trace_id)
                
            self.height_var.set(str(new_height))
            self.height_trace_id = self.height_var.trace_add("write", self.update_width_from_height)
        except (ValueError, ZeroDivisionError):
            pass
    
    def update_width_from_height(self, *args):
        """Update width based on height to maintain aspect ratio"""
        if not self.aspect_lock.get() or not self.selected_file:
            return
        
        try:
            height = int(self.height_var.get())
            new_width = int(round(height * self.aspect_ratio))
            
            if self.width_trace_id:
                self.width_var.trace_remove("write", self.width_trace_id)
                
            self.width_var.set(str(new_width))
            self.width_trace_id = self.width_var.trace_add("write", self.update_height_from_width)
        except (ValueError, ZeroDivisionError):
            pass
    
    def update_status(self, message, status_type="info"):
        """Update status message with color coding in the Text widget"""
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.tag_add(status_type, "end-1l", "end")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
    
    def start_resize_thread(self):
        """Start the resizing process in a separate thread"""
        threading.Thread(target=self.resize_image, daemon=True).start()
    
    def resize_image(self):
        """Handle the image resizing and saving process."""
        if not self.selected_file:
            self.update_status("Please select an image first", "error")
            return
        
        self.progress.start()
        self.resize_button.config(state=tk.DISABLED)
        
        selected_folder = self.selected_folder_var.get()
        new_filename = self.new_filename_var.get()
        selected_format = self.format_var.get().lower()
        
        if not selected_folder or selected_folder == "No folder selected":
            self.update_status("Please choose a destination folder", "error")
            self.progress.stop()
            self.resize_button.config(state=tk.NORMAL)
            return
        
        if not new_filename:
            self.update_status("Please enter a filename", "error")
            self.progress.stop()
            self.resize_button.config(state=tk.NORMAL)
            return
        
        # Auto-append extension if missing and format is specified
        if selected_format != "same as input" and not new_filename.lower().endswith(f".{selected_format}"):
            new_filename += f".{selected_format}"
            self.new_filename_var.set(new_filename)
        
        width_str = self.width_var.get()
        height_str = self.height_var.get()
        
        if not width_str.isdigit() or not height_str.isdigit():
            self.update_status("Please enter positive integers for width and height", "error")
            self.progress.stop()
            self.resize_button.config(state=tk.NORMAL)
            return
        
        width = int(width_str)
        height = int(height_str)
        
        if width <= 0 or height <= 0:
            self.update_status("Width and height must be greater than zero", "error")
            self.progress.stop()
            self.resize_button.config(state=tk.NORMAL)
            return
        
        try:
            img = Image.open(self.selected_file)
            resized_img = img.resize((width, height), Image.LANCZOS)
            output_path = os.path.join(selected_folder, new_filename)
            
            # Handle format conversion if needed
            if selected_format != "same as input":
                base, _ = os.path.splitext(output_path)
                output_path = f"{base}.{selected_format}"
            
            # Save with quality parameter for JPG
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                resized_img.save(output_path, quality=self.quality_var.get())
            else:
                resized_img.save(output_path)
            
            self.update_status(f"Image resized and saved as {output_path}", "success")
        except Exception as e:
            self.update_status(f"Error resizing image: {str(e)}", "error")
            messagebox.showerror("Error", str(e))
        
        self.progress.stop()
        self.resize_button.config(state=tk.NORMAL)

# Application startup
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedImageResizer(root)
    root.mainloop()