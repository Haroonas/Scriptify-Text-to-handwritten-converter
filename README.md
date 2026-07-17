# 🖋️ Scriptify - Digital Ink Engine

Scriptify is a web application that allows users to convert digital text into realistic handwriting. Built with Python, Flask, and the Pillow library, the application takes user input and renders it onto a digital paper texture using various custom handwriting fonts.

## ✨ Features
* ✍️ **Multiple Handwriting Styles:** Choose from various TrueType fonts to match different handwriting aesthetics.
* 📏 **Automatic Word Wrapping:** The backend calculation ensures text naturally wraps within the margins of the generated page.
* 🖼️ **Dynamic Previews:** Automatically generates preview images for any fonts placed in the fonts directory.
* 💾 **Direct Download:** Users can save their generated handwritten documents directly to their device.

## 🛠️ Tech Stack
* ⚙️ **Backend:** Python, Flask
* 🎨 **Image Processing:** Pillow (PIL)
* 🖥️ **Frontend:** HTML, Tailwind CSS

## 💻 Local Setup
1. Clone the repository to your local machine.
2. Install the required dependencies:
   `pip install -r requirements.txt`
3. Run the Flask development server:
   `python main.py`
4. Open a web browser and navigate to `http://127.0.0.1:5000`

## 📂 Directory Structure
* 🔤 `/fonts` - Drop any `.ttf` files here to automatically add them as handwriting styles.
* 🖼️ `/images` - Stores the generated user outputs.
* 📸 `/images/previews` - Automatically generated thumbnails for the font selection UI.
* 📄 `/templates` - Contains the HTML frontend.
