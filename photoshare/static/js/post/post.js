var EditComment = function (commentpk) {
	var comment_wrap = document.getElementById('comment_' + commentpk);
	var comment = comment_wrap.children[3];
	var comment__edit_form = comment_wrap.children[4];
	comment.style.display = 'none';
	comment__edit_form.style.display = 'block';
};