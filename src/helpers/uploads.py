import config
import os
import random
import string
import sys
from werkzeug import secure_filename


def process(files):

	urls = []

	for f in files:
		f = files[f]
		ext = f.filename.split('.')[-1]

		if ext in config.ALLOWED_AUDIO:
			filename = save(f, ext)
			urls.append('"/a/{}"'.format(filename))

		elif ext in config.ALLOWED_IMAGE:
			filename = save(f, ext)
			urls.append('"/i/{}"'.format(filename))

		elif ext in config.ALLOWED_FILE:
			filename = save(f, ext)
			urls.append('"/f/{}"'.format(filename))

		elif ext in config.ALLOWED_TEXT:
			ext = 'txt'
			filename = save(f, ext)
			urls.append('"/t/{}"'.format(filename))

		elif ext in config.ALLOWED_VIDEO:
			filename = save(f, ext)
			urls.append('"/v/{}"'.format(filename))

	return urls


def save(f, ext):

	filename = secure_filename(filename_gen() + '.' + ext)

	if ext is 'txt':
		folder = '/text'
	elif ext in config.ALLOWED_AUDIO:
		folder = '/audio'
	elif ext in config.ALLOWED_FILE:
		folder = '/file'
	elif ext in config.ALLOWED_IMAGE:
		folder = '/image'
	elif ext in config.ALLOWED_VIDEO:
		folder = '/video'

	filepath = os.path.join(config.UPLOAD_TO + folder, filename)

	file_exists = os.path.isfile(filepath)
	while file_exists is True:
		filename = secure_filename(filename_gen() + '.' + ext)
		filepath = os.path.join(config.UPLOAD_TO + folder, filename)

	f.save(filepath)

	return filename


def filename_gen(size=4, chars=string.ascii_lowercase):

	return ''.join(random.choice(chars) for _ in range(size))
