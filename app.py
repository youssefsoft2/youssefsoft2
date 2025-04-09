from flask import Flask, render_template, request, send_file
from moviepy.editor import *
import os

app = Flask(__name__)

# مجلد لتحزين الصور والفيديوهات المؤقتة
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'لا توجد صورة'
    
    image = request.files['image']
    
    if image.filename == '':
        return 'لم يتم اختيار صورة'
    
    # حفظ الصورة
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    
    # توليد الفيديو من الصورة
    clip = ImageClip(image_path, duration=5)  # 5 ثواني
    clip = clip.set_fps(24)
    
    # حفظ الفيديو
    video_path = os.path.join(UPLOAD_FOLDER, 'output.mp4')
    clip.write_videofile(video_path, fps=24)
    
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
