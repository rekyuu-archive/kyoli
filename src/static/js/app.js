const manual 	= document.getElementById('manual');
const dropin	= document.getElementById('dropin');
const urlist	= document.getElementById('urlist');
const pretext	= document.getElementById('pre');
const postext	= document.getElementById('post');
const errtext	= document.getElementById('err');
const niltext	= document.getElementById('nil');

// Opens the file browser.
function manual_open (e) {
	e.preventDefault();
	manual.click();
}

// Uploads from the file browser if it changes.
function manual_upload (e) {
	var files = manual.files;
	upload(files);
}

// Detects if something was dragged into the window.
function drag (e) {
	e.stopPropagation();
	e.preventDefault();
}

// Detects if something was dropped into the window.
function drop (e) {
	drag(e);
	var files = e.dataTransfer.files;
	upload(files);
}

// Performs a POST of pasted text.
function paste (e) {
	var pasted = e.clipboardData.getData('text/plain');
	var blob = new Blob([pasted], {type: 'text/plain'});
	var file = new File([blob], 'paste.txt');
	var files = [file];
	upload(files);
}

// Performs the POST function to the server.
function upload (files) {
	postext.style.display = 'block';
	pretext.style.display = 'none';
	niltext.style.display = 'none';
	errtext.style.display = 'none';

	if (files.length > 0) {
		var form = new FormData();

		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			form.append('file_' + i, file, file.name);
		}

		var req = new XMLHttpRequest();
		req.open('POST', '/api/upload', true);

		req.onload = function () {
			var response = JSON.parse(req.response);
			if (response.status == 'ok') {
				if (response.urls.length == 1 ) {
					window.location = response.urls[0];
				} else {
					dropin.style.display = 'none';
					urlist.style.display = 'block';

					for (var i = 0; i < response.urls.length; i++) {
						var link = document.createElement('a');
						link.setAttribute('href', response.urls[i]);
						link.setAttribute('target', '_blank');
						link.innerHTML = '<p>' + response.urls[i] + '</p>';
						urlist.appendChild(link);
					}
				}
			} else if (response.status == 'none' ) {
				niltext.style.display = 'block';
				postext.style.display = 'none';
			} else {
				errtext.style.display = 'block';
				postext.style.display = 'none';
			}
		}

		req.send(form);
	}
}

// Adds the event listeners.
manual.addEventListener('change', manual_upload, false);
dropin.addEventListener('click', manual_open, false);
window.addEventListener('drop', drop, false);
window.addEventListener('dragenter', drag, false);
window.addEventListener('dragleave', drag, false);
window.addEventListener('dragover', drag, false);
window.addEventListener('paste', paste, false);
