$(document).ready(function () {
	var description__edit_button = document.getElementById('description__edit_button');
	var description__edit_form = document.getElementById('description__edit_form');
	var description = document.getElementById('description');

	description__edit_button.addEventListener('click', function () {
		description.style.display = 'none';
		description__edit_form.style.display = 'block';
	});
});