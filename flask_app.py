from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    if request.method == "POST":
        musica = request.form.get("musica")
        if musica:
            try:
                # Cria pasta temporária
                temp_dir = tempfile.mkdtemp()
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                }
                
                # Define URL ou pesquisa
                url = musica if musica.startswith("http") else f"ytsearch1:{musica}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                
                return send_file(filename, as_attachment=True)
            except Exception as e:
                mensagem = f"Erro: {e}"
        else:
            mensagem = "Digite o nome da música ou link!"
    return render_template("index.html", mensagem=mensagem)
    
if __name__ == "__main__":
    app.run(debug=True)
