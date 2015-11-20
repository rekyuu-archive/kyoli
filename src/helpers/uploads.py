import config
from enum import Enum
import hashlib
import os
import random
import string
import sqlite3 as sql
import sys
from werkzeug import secure_filename


class FileType(Enum):


	none  = "none"
	audio = "audio"
	image = "image"
	files = "file"
	text  = "text"
	video = "video"


def process(files):

	urls = []

	for f in files:
		f = files[f]
		ext = f.filename.split('.')[-1]
		filetype = FileType.none

		if ext in config.ALLOWED_AUDIO:
			filetype = FileType.audio
		elif ext in config.ALLOWED_IMAGE:
			filetype = FileType.image
		elif ext in config.ALLOWED_FILE:
			filetype = FileType.files
		elif ext in config.ALLOWED_TEXT:
			ext = 'txt'
			filetype = FileType.text
		elif ext in config.ALLOWED_VIDEO:
			filetype = FileType.video

		if filetype is not FileType.none:
			url = save_and_get_url(f, ext, filetype)
			urls.append('"{}"'.format(url))
		else:
			urls.append('"rejected: {} (not allowed)"'.format(f.filename))

	return urls


def save_and_get_url(f, ext, filetype):

	if filetype is FileType.audio:
		folder = '/audio'
		url = '/a/'
	elif filetype is FileType.files:
		folder = '/file'
		url = '/f/'
	elif filetype is FileType.image:
		folder = '/image'
		url = '/i/'
	elif filetype is FileType.text:
		folder = '/text'
		url = '/t/'
	elif filetype is FileType.video:
		folder = '/video'
		url = '/v/'

	check = check_if_exists(f, ext, filetype)
	exists = check[0]
	filename = check[1]

	if exists:
		filepath = os.path.join(config.UPLOAD_TO + folder, filename)
		f.save(filepath)

	url += filename

	return url


def check_if_exists(f, ext, filetype):

	md5 = get_md5_hash(f)

	con = sql.connect(config.UPLOAD_TO + '/' + config.DATABASE)
	with con:
		con.row_factory = sql.Row
		db = con.cursor()

		db.execute(
			"""
			CREATE TABLE IF NOT EXISTS Uploads(
				id INTEGER PRIMARY KEY,
				filename TEXT,
				md5 TEXT,
				filetype TEXT
			)
			"""
		)

		filename = db.execute(
			"""
			SELECT filename FROM Uploads
			WHERE filetype = ?
			AND md5 = ?
			""",
			(str(filetype), md5)
		).fetchone()

		if filename is None:
			save = True
			filename = secure_filename(get_random_filename() + '.' + ext)
			db.execute(
				"""
				INSERT INTO Uploads(filename, md5, filetype)
				VALUES (?, ?, ?)
				""",
				(filename, md5, str(filetype))
			)
		else:
			save = False
			filename = filename['filename']

	return (save, filename)


def get_md5_hash(f):

	hasher = hashlib.md5()
	hasher.update(f.read())
	f.seek(0)
	md5_hash = hasher.hexdigest()

	return md5_hash


def get_random_filename(size=4, chars=string.ascii_lowercase):

	return ''.join(random.choice(chars) for _ in range(size))
