# Enhanced Image Resizer

## Description
This Python script provides a graphical user interface (GUI) tool for resizing images. It allows users to select an image, adjust its dimensions, preview the result, and save the resized image to a chosen destination folder. The script includes features like aspect ratio locking, format conversion, quality adjustment for JPGs, and preset sizes, making it a versatile tool for image manipulation.

## Features
- **Image Selection**: Browse and load images (JPG, PNG, BMP, GIF).
- **Resize Options**: Set custom width and height or choose from preset sizes (e.g., Thumbnail, HD).
- **Aspect Ratio Lock**: Maintain the original aspect ratio when adjusting dimensions.
- **Format Conversion**: Save in JPG, PNG, BMP, GIF, or keep the original format.
- **JPG Quality Slider**: Adjust compression quality for JPG output (1-100).
- **Preview**: Display a thumbnail preview of the selected image.
- **Destination Folder**: Choose where to save the resized image with a custom filename.
- **Progress Indicator**: Shows processing status during resizing.
- **Status Log**: Displays success, error, or info messages in a color-coded log.
- **Keyboard Shortcuts**: Quick access to browse (Ctrl+O), resize (Ctrl+S), and choose folder (Ctrl+D).
- **Config Persistence**: Remembers the last used destination folder via a JSON config file.

## Requirements
- Python 3.x
- Tkinter (usually included with Python; install via `pip install tk` if missing)
- Pillow (PIL) library (`pip install Pillow`)

## Usage
1. **Run the Script**:
   - Save the script as `enhanced_image_resizer.py`.
   - Install the required Pillow library if not already present: `pip install Pillow`.
   - Execute it with Python: `python enhanced_image_resizer.py`.
   - A GUI window titled "Enhanced Image Resizer" will appear.

2. **Select an Image**:
   - Click "Browse Image" or press `Ctrl+O`.
   - Choose an image file (e.g., `photo.jpg`) from your filesystem.
   - The original dimensions will display, and a preview will appear.

3. **Configure Resize Settings**:
   - Enter a new width and height in pixels, or select a preset size (e.g., "HD (1280x720)") from the dropdown.
   - Check "Maintain aspect ratio" to lock proportions (default: enabled).
   - Choose an output format from the "Format" dropdown (default: "Same as input").
   - Adjust the "JPG Quality" slider if saving as JPG (default: 85).

4. **Set Output Options**:
   - Enter a new filename (default: `originalname_resized.ext`).
   - Click "Choose Destination Folder" or press `Ctrl+D` to select a save location (last folder is remembered).
   - The selected folder path will display below.

5. **Resize and Save**:
   - Click "Resize and Save" or press `Ctrl+S`.
   - A progress bar will animate during processing.
   - Check the status log for success or error messages.
   - The resized image will be saved to the specified folder.

## Example Workflow
- Load `photo.jpg` (1920x1080).
- Set width to 1280, height adjusts to 720 (aspect ratio locked).
- Choose "JPG" format, quality 90.
- Set filename to `photo_resized.jpg` and destination to `C:\output`.
- Click "Resize and Save".
- Output: `C:\output\photo_resized.jpg` (1280x720).

## Output
- **Status Log**: Messages like:
  - "Image selected successfully" (green)
  - "Image resized and saved as C:\output\photo_resized.jpg" (green)
  - "Error resizing image: ..." (red)
- **Saved File**: The resized image in the chosen format and location.

## Notes
- **File Extensions**: If the filename lacks an extension and a specific format is chosen, it’s auto-appended (e.g., `photo` becomes `photo.jpg` for JPG).
- **Config File**: Saves the last destination folder to `image_resizer_config.json` in the script’s directory.
- **Threading**: Resizing runs in a separate thread to keep the GUI responsive.
- **Validation**: Ensures width/height are positive integers; displays errors if invalid.
- **Customization**: Modify preset sizes or add new formats by editing the `set_preset_size` or `format_menu` sections.

## Known Limitations
- Does not support batch processing (single image only).
- Requires Pillow for image handling; ensure it’s installed.

## License
This script is provided as-is for personal or educational use. Feel free to modify it to suit your needs!
