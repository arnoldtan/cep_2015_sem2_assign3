var pendingToDelete = function (userId) {
	var delete_follow_button = document.getElementById('delete_follow_button_' + userId);
	delete_follow_button.innerHTML = 'Delete';
	delete_follow_button.classList.remove('button-warning');
	delete_follow_button.classList.add('button-error');
}

var deleteToPending = function (userId) {
	var delete_follow_button = document.getElementById('delete_follow_button_' + userId);
	delete_follow_button.innerHTML = 'Pending';
	delete_follow_button.classList.remove('button-error');
	delete_follow_button.classList.add('button-warning');
}