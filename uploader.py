import sys, os, string, random
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename


# Flask initialization.
app = Flask(__name__)


# Uploader defaults for location and filetypes.
UPLOAD_FOLDER = '/var/www/uploader/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webm', 'mp4', 'mp3',
                          'flac', 'ogg', 'txt', 'pdf', 'css', 'htm', 'html',
                          'js', 'py', 'sh', 'conf'])
TEXT_EXTENSIONS = set(['css', 'htm', 'html', 'js', 'py', 'sh', 'conf'])


# Configuration for Flask.
app.config['UPLOAD_FOLDER']      = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


# Checks if the file is allowed.
def allowed_file(filename):

   return '.' in filename and \
      filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Generates a four-character name for the file.
def id_generator(size=4, chars=string.ascii_lowercase):

   return ''.join(random.choice(chars) for _ in range(size))


# Handles image uploading.
@app.route('/', methods=['GET', 'POST'])
def upload_file():

   if request.method == 'POST':

      # Retrieves the file and checks if it is allowed.
      file = request.files['file']
      if file and allowed_file(file.filename):

         # If it is one of the above text extensions, renames the extension to
         # a text file for safety reasons.
         file_ext = file.filename.rsplit('.', 1)[1]
         if file_ext in TEXT_EXTENSIONS:
            file_ext = 'txt'

         # Creates a random ID for the saved file.
         rand_id  = id_generator()
         filename = secure_filename(rand_id + '.' + file_ext)
         filepath = os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         # Loops if the filename exists, until it generates a unique name.
         while filepath == True:
            rand_id  = id_generator()
            filename = secure_filename(rand_id + '.' + file_ext)
            filepath = os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         # Saves the file.
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         # Text files are displayed at /u, while images are displayed at root.
         if file_ext == 'txt':
            return redirect('http://kyo.li/u/' + rand_id, code=302)
         else:
            return redirect('http://kyo.li/' + rand_id, code=302)

   return render_template('index.html')


# Displays a text file at /u/file.
@app.route('/<text>')
def uploaded_file(text):
   textfile = open(app.config['UPLOAD_FOLDER'] + '/' + text + '.txt').read()
   return render_template('text.html', text = textfile)


# Runs the script.
if __name__ == '__main__':
   app.debug = False
   app.run()
