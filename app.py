from flask import Flask, render_template, request
import os, youtube_dl
from flask.helpers import url_for

app = Flask(__name__)
urllink = ""

@app.route('/')
def home():
	downloads = os.listdir(os.path.join(app.static_folder, 'downloads'))

	return render_template('home.html', files=downloads)

def hook(response):
	global urllink
	urllink = response['filename'].replace('.f98', '').replace('/static/', '')

@app.route('/ytdl/', methods=['POST'])
def ytdl():
	link = request.data.decode('utf-8')

	os.chdir(app.static_folder + "/downloads/")
	ydl_opts = {
		"progress_hooks": [hook],
		"quiet": True if True else False,
		"geo-bypass": True
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			code = ydl.download([link])
	except Exception:
		return {"error": True}

	if code != 0 or urllink == "":
		return {"error": True}

	
	return {"error": False, "data": urllink}

if __name__ == '__main__':
    app.run(debug=True)
