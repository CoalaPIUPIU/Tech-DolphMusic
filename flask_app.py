from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    file_ready = False
    filename = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                "quiet": True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info_dict)
                    file_ready = True
            except Exception as e:
                return f"Erro ao baixar: {e}"

    return render_template("index.html", file_ready=file_ready, filename=filename)

@app.route("/download/<path:filename>")
def download(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Arquivo não encontrado!", 404

if __name__ == "__main__":
    app.run(debug=True)
