# from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image, ImageDraw
# import numpy as np
# import os
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['OUTPUT_FOLDER'] = 'static/outputs/'
# LABELS = {
#     "#fedd3a": "vegetation",
#     "#e2a929": "water_bodies",
#     "#6ec1e4": "roads",
#     "#3c1098": "build_up",
#     "#8429f6": "barren_land"
# }
# def process_images(mask_image_path, original_image_path):
#     mask_img= Image.open(mask_image_path)
#     original_img =Image.open(original_image_path)
#     if mask_img.mode!= 'RGB':
#         mask_img =mask_img.convert('RGB')
#     if original_img.mode!= 'RGB':
#         original_img=original_img.convert('RGB')
#     if mask_img.size !=original_img.size:
#         original_img =original_img.resize(mask_img.size)
#     mask_data =np.array(mask_img)
#     original_data=np.array(original_img)
#     color_map ={tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)): label for h, label in LABELS.items()}
#     pixel_counts ={label: 0 for label in LABELS.values()}
#     labeled_images={label: Image.new('RGB', mask_img.size, color=(0, 0, 0)) for label in LABELS.values()}
#     draw_maps ={label: ImageDraw.Draw(labeled_images[label]) for label in LABELS.values()}
#
#
#     for y in range(mask_data.shape[0]):
#         for x in range(mask_data.shape[1]):
#             pixel= tuple(mask_data[y, x][:3])
#             if pixel in color_map:
#                 label =color_map[pixel]
#                 pixel_counts[label] += 1
#                 original_pixel= tuple(original_data[y, x][:3])
#                 draw_maps[label].point((x, y), fill=original_pixel)
#     for label, image in labeled_images.items():
#         output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{label}.png")
#         image.save(output_path)
#     return pixel_counts
#
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         if 'mask_file' not in request.files or 'original_file' not in request.files:
#             return redirect(request.url)
#         mask_file= request.files['mask_file']
#         original_file =request.files['original_file']
#         if mask_file.filename =='' or original_file.filename == '':
#             return redirect(request.url)
#         if mask_file and original_file:
#             mask_filename =mask_file.filename
#             original_filename =original_file.filename
#             mask_filepath= os.path.join(app.config['UPLOAD_FOLDER'], mask_filename)
#             original_filepath =os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
#             mask_file.save(mask_filepath)
#             original_file.save(original_filepath)
#             pixel_counts =process_images(mask_filepath, original_filepath)
#             return render_template('index.html', pixel_counts=pixel_counts, output_folder=app.config['OUTPUT_FOLDER'])
#     return render_template('index.html')
#
#
# if __name__ == "__main__":
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
#     if not os.path.exists(app.config['OUTPUT_FOLDER']):
#         os.makedirs(app.config['OUTPUT_FOLDER'])
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from PIL import Image, ImageDraw
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'static/outputs/'

LABELS = {
    "#fedd3a": "vegetation",
    "#e2a929": "water_bodies",
    "#6ec1e4": "roads",
    "#70bfe1": "roads",
    "#77bde1": "roads",
    "#3c1099": "build_up",
    "#3c1098": "build_up",
    "#8429f6": "barren_land",
    "#8529f6": "barren_land"
}

def process_images(mask_image_path, original_image_path):
    mask_img = Image.open(mask_image_path)
    original_img = Image.open(original_image_path)

    if mask_img.mode != 'RGB':
        mask_img = mask_img.convert('RGB')
    if original_img.mode != 'RGB':
        original_img = original_img.convert('RGB')
    if mask_img.size != original_img.size:
        original_img = original_img.resize(mask_img.size)

    mask_data = np.array(mask_img)
    original_data = np.array(original_img)

    color_map = {tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)): label for h, label in LABELS.items()}
    pixel_counts = {label: 0 for label in LABELS.values()}
    labeled_images = {label: Image.new('RGB', mask_img.size, color=(0, 0, 0)) for label in LABELS.values()}
    draw_maps = {label: ImageDraw.Draw(labeled_images[label]) for label in LABELS.values()}

    total_pixels = mask_data.shape[0] * mask_data.shape[1]

    for y in range(mask_data.shape[0]):
        for x in range(mask_data.shape[1]):
            pixel = tuple(mask_data[y, x][:3])
            if pixel in color_map:
                label = color_map[pixel]
                pixel_counts[label] += 1
                original_pixel = tuple(original_data[y, x][:3])
                draw_maps[label].point((x, y), fill=original_pixel)

    for label, image in labeled_images.items():
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{label}.png")
        image.save(output_path)

    return pixel_counts, total_pixels

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'mask_file1' not in request.files or 'original_file1' not in request.files or \
           'mask_file2' not in request.files or 'original_file2' not in request.files:
            return redirect(request.url)

        mask_file1 = request.files['mask_file1']
        original_file1 = request.files['original_file1']
        mask_file2 = request.files['mask_file2']
        original_file2 = request.files['original_file2']

        if mask_file1.filename == '' or original_file1.filename == '' or \
           mask_file2.filename == '' or original_file2.filename == '':
            return redirect(request.url)

        if mask_file1 and original_file1 and mask_file2 and original_file2:
            mask_filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], mask_file1.filename)
            original_filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], original_file1.filename)
            mask_filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], mask_file2.filename)
            original_filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], original_file2.filename)

            mask_file1.save(mask_filepath1)
            original_file1.save(original_filepath1)
            mask_file2.save(mask_filepath2)
            original_file2.save(original_filepath2)

            pixel_counts1, total_pixels1 = process_images(mask_filepath1, original_filepath1)
            pixel_counts2, total_pixels2 = process_images(mask_filepath2, original_filepath2)

            pixel_differences = {label: pixel_counts2[label] - pixel_counts1[label] for label in LABELS.values()}
            urbanization_pixels = pixel_differences.get("roads", 0) + pixel_differences.get("build_up", 0)
            urbanization_percentage = (urbanization_pixels / total_pixels2) * 100 if total_pixels2 else 0

            return render_template('index.html', pixel_counts1=pixel_counts1, pixel_counts2=pixel_counts2,
                                   pixel_differences=pixel_differences, urbanization_percentage=urbanization_percentage,
                                   output_folder=app.config['OUTPUT_FOLDER'])

    return render_template('index.html')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    app.run(debug=True, port=5002)
