$(document).ready(function () {
	if (window.location.hash === '#signupform') {
		if (window.location.search.length > 0) {
			var receivedErrors = window.location.search.slice(1).split('%0A')
			var errorList = document.createElement('ul');
			errorList.classList.add("errors");

			for (var i=0; i<receivedErrors.length - 1; ++i) {
				var error = document.createElement('li');
				error.innerHTML = receivedErrors[i].split('-').join(' ');
				errorList.appendChild(error);
			}
			document.getElementById('signupform').appendChild(errorList)
		}
	}

	if (window.location.hash === '#loginform') {
		if (window.location.search.length > 0) {
			var receivedErrors = window.location.search.slice(1).split('%0A')
			var errorList = document.createElement('ul');
			errorList.classList.add("errors");

			for (var i=0; i<receivedErrors.length - 1; ++i) {
				var error = document.createElement('li');
				error.innerHTML = receivedErrors[i].split('-').join(' ');
				errorList.appendChild(error);
			}
			document.getElementById('loginform').appendChild(errorList)
		}
	}
})