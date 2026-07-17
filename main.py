from flask import Flask, render_template, request, url_for
from PIL import Image, ImageDraw, ImageFont
import os
import time

app = Flask(__name__, static_folder='images')

# --- CONFIGURATION ---
FONTS_DIR = "fonts"
IMAGES_DIR = "images"
PREVIEWS_DIR = os.path.join(IMAGES_DIR, "previews")

# --- AUTO-GENERATE PERFECT PREVIEWS (WITH MANUAL TWEAKS) ---
if not os.path.exists(PREVIEWS_DIR):
    os.makedirs(PREVIEWS_DIR)

if os.path.exists(FONTS_DIR):
    for filename in os.listdir(FONTS_DIR):
        if filename.endswith(".ttf"):
            preview_name = filename.replace(".ttf", ".png")
            save_path = os.path.join(PREVIEWS_DIR, preview_name)
            
            if not os.path.exists(save_path):
                img = Image.new('RGB', (400, 150), color='white')
                draw = ImageDraw.Draw(img)
                font_path = os.path.join(FONTS_DIR, filename)
                
                sample_text = "Sample Text"
                
                # 1. SET SIZE: Gloria needs to be smaller to fit
                font_size = 45 if "Gloria" in filename else 60
                
                try:
                    preview_font = ImageFont.truetype(font_path, font_size)
                except:
                    preview_font = ImageFont.load_default()
                
                # 2. SET POSITION: The "mm" anchor is the center point
                # Default center is (200, 75)
                target_x = 200
                target_y = 75
                
                # 3. THE "GLORIA FIX": Manual nudge for that specific font
                if "Gloria" in filename:
                    target_x += 10  # Nudge RIGHT
                    target_y += 5   # Nudge down
                
                # Draw using the anchor point for the most stable alignment
                draw.text((target_x, target_y), sample_text, font=preview_font, fill=(0, 0, 0), anchor="mm")
                
                img.save(save_path)
# --- THE WEBSITE LOGIC ---
@app.route('/', methods=['GET', 'POST'])
def index():
    font_options = []
    if os.path.exists(FONTS_DIR):
        for filename in os.listdir(FONTS_DIR):
            if filename.endswith(".ttf"):
                preview_name = filename.replace(".ttf", ".png")
                font_options.append({
                    'filename': filename,
                    'name': filename.replace("-", " ").replace(".ttf", "").split('-')[0],
                    'preview': f"previews/{preview_name}"
                })

    result_image = None

    if request.method == 'POST':
        user_text = request.form.get('text_input')
        selected_font = request.form.get('font_selection')

        paper = Image.new("RGB", (800, 1000), 'white')
        pen = ImageDraw.Draw(paper)

        font_path = os.path.join(FONTS_DIR, selected_font)
        try:
            font = ImageFont.truetype(font_path, 40)
        except:
            font = ImageFont.load_default()

        # Alignment Logic
        ink_color = (0, 0, 150)
        left_margin, right_margin, line_height = 50, 750, 50
        current_x, current_y = left_margin, 50
        space_width = pen.textlength(" ", font=font)

        lines = user_text.replace('\r\n', '\n').split('\n')

        for line in lines:
            if line == "":
                current_y += line_height
                continue
            words = line.split(' ')
            current_x = left_margin
            for word in words:
                if word == "":
                    current_x += space_width
                    continue
                word_width = pen.textlength(word, font=font)
                if current_x + word_width > right_margin:
                    current_x, current_y = left_margin, current_y + line_height
                pen.text((current_x, current_y), word, font=font, fill=ink_color)
                current_x += word_width + space_width
            current_y += line_height

        timestamp = int(time.time())
        output_filename = f"result_{timestamp}.png"
        paper.save(os.path.join(IMAGES_DIR, output_filename))
        result_image = output_filename

    return render_template('index.html', fonts=font_options, result=result_image)

if __name__ == '__main__':
    app.run(debug=True)
