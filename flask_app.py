from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Caminho do arquivo de cookies que você vai subir pro servidor
COOKIES_FILE = 'youtube_cookies.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_path = 'downloads/%(title)s.%(ext)s'

    ydl_opts = {
        'outtmpl': output_path,
        'cookiefile': COOKIES_FILE,  # <- adiciona cookies aqui
        'format': 'bestaudio/best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f'Erro ao baixar: {str(e)}'

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000)
