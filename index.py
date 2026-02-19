from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_url(url):
    ydl_opts = {
    'format': 'best[height<=1080]',
    'noplaylist': True,
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.basename(filename)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        video_url = request.form.get("url")

        if not video_url:
            return render_template("index.html", error="Please enter a valid URL!")

        try:
            filename = download_url(video_url)
            return render_template("index.html", success="Download completed!", filename=filename)

        except Exception as e:
            return render_template("index.html", error=f"Error: {str(e)}")

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

