import config
import os
from helpers import uploads
from flask import Flask, request, redirect, render_template, make_response, \
	send_file, Markup


if not os.path.exists(config.UPLOAD_TO):
	os.makedirs(config.UPLOAD_TO)
	os.makedirs(config.UPLOAD_TO + '/audio')
	os.makedirs(config.UPLOAD_TO + '/file')
	os.makedirs(config.UPLOAD_TO + '/image')
	os.makedirs(config.UPLOAD_TO + '/text')
	os.makedirs(config.UPLOAD_TO + '/video')


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_SIZE_MB * 1024 * 1024


@app.route('/')
def index():

	return render_template('index.html')

@app.route('/a/<audio>')
def render_audio(audio):

	location = config.UPLOAD_TO + '/audio/' + audio
	return send_file(location)

@app.route('/f/<file_>')
def render_file(file_):

	location = config.UPLOAD_TO + '/file/' + file_
	return send_file(location)

@app.route('/i/<image>')
def render_image(image):

	location = config.UPLOAD_TO + '/image/' + image
	return send_file(location)

@app.route('/t/<text>')
def render_text(text):

	with open(config.UPLOAD_TO + '/text/' + text) as t:
		out = t.read()
		return render_template('text.html', text=out)

@app.route('/v/<video>')
def render_video(video):

	location = config.UPLOAD_TO + '/video/' + video
	return render_template('video.html', video=video)

@app.route('/about')
def page_about():

	header = 'about kyo.li'
	text = """
	<b>max file size:</b> 50mb <br />
	<br />
	<br />
	<b>accepted audio:</b> &nbsp;['flac', 'mp3', 'ogg'] <br />
	<b>accepted images:</b> ['gif', 'jpg', 'jpeg', 'png'] <br />
	<b>accepted files:</b> &nbsp;['pdf'] <br />
	<b>accepted text:</b> &nbsp;&nbsp;['css', 'conf', 'htm', 'html', 'js',
		'py', 'sh', 'txt'] <br />
	<b>accepted video:</b> &nbsp;['mp4', 'webm'] <br />
	<br />
	<br />
	created by <b>rekyuu</b> <br />
	<br />
	<br />
	<b>website:</b> <a href="http://rekyuu.co/">
		http://rekyuu.co/
	</a> <br />
	<b>github:</b>&nbsp;<a href="https://github.com/rekyuu">
		https://github.com/rekyuu
	</a> <br />
	<b>twitter:</b> <a href="https://twitter.com/rekyuu_senkan">
		https://twitter.com/rekyuu_senkan
	</a> <br />
	"""
	text = Markup(text)

	return render_template('page.html', header=header, text=text)

@app.route('/api')
def page_api():

	header = 'api usage'
	text = """
	<b>POST /api/upload</b> <br />
	<br />
	returns JSON: {<b>"status"</b>: "ok",
		<b>"urls"</b>: ["list", "of", "urls"]} <br />
	<br />
	if none of the files succeed: {<b>"status"</b>: "none"}
	"""
	text = Markup(text)

	return render_template('page.html', header=header, text=text)

@app.route('/api/video/<video>')
def api_video(video):

	location = config.UPLOAD_TO + '/video/' + video
	return send_file(location)

@app.route('/api/upload', methods=['POST'])
def api_upload():

	files = request.files
	urls = uploads.process(files)

	if len(urls) >= 1:
		response = '{"status": "ok", "urls": ['
		for url in urls:
			response += '{}, '.format(url)
		response = response[:-2]
		response += ']}'
	else:
		response = '{"status": "none"}'

	print(response)
	resp = make_response(response)
	resp.headers['Content-Type'] = "application/json"
	return resp


if __name__ == '__main__':

	app.debug = config.DEBUG
	app.run(threaded=True, host='0.0.0.0', port=config.PORT)
