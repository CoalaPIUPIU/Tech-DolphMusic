from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            return render_template("index.html", error="Insira a URL do vídeo!")

        # Configuração do yt-dlp
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "ignoreerrors": True,  # evita erro em vídeos que precisam login
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                if info_dict is None:
                    return render_template("index.html", error="Não foi possível baixar o vídeo.")
                filename = ydl.prepare_filename(info_dict)
                return send_file(filename, as_attachment=True)
        except Exception as e:
            return render_template("index.html", error=f"Erro: {str(e)}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
