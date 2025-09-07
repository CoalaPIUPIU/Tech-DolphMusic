from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# garante que a pasta existe
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_song():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Nenhuma URL fornecida"}), 400

    # opções do yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        'cookiefile': 'cookies.txt',  # <- arquivo que você criou
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        return send_file(filename, as_attachment=True)
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Erro ao baixar: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
