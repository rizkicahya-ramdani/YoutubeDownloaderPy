from flask import Flask, render_template, request, send_file, flash
from pytube import YouTube
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'do-not-use-this-in-production' 

DOWNLOAD_FOLDER = "downloads"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    if not video_url:
        flash("Silakan masukkan URL YouTube.", "error")
        return render_template('index.html')

    try:
        logging.info(f"Mencoba mengunduh dari URL: {video_url}")
        yt = YouTube(video_url)

        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        
        logging.info(f"Mengunduh '{yt.title}'...")
        file_path = stream.download(output_path=DOWNLOAD_FOLDER)
        logging.info(f"Video berhasil diunduh ke: {file_path}")
        
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Terjadi kesalahan: {str(e)}")
        flash(f"Gagal mengunduh video. Pastikan URL valid dan coba lagi. (Error: {str(e)})", "error")
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)