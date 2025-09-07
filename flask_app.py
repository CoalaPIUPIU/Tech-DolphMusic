<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Tech Dolph Music</title>
</head>
<body>
    <h1>Tech Dolph Music Downloader</h1>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        <input type="text" name="video_url" placeholder="Cole a URL do vídeo aqui" style="width:300px;">
        <button type="submit">Baixar Música</button>
    </form>
</body>
</html>
