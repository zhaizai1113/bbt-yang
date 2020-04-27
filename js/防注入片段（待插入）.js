function htmlEncode(str){
	var ele = document.createElement('span');
	ele.appendChild(document.createTextNode(str));
	return ele.innerHTML;
}
function htmlDecode(str){
	var ele = document.createElement('span');
	ele.innerHTML=str;
	return ele.textContent;
}
var msg = htmlRncodeJQ('<script>alert('test');</script>');
$('body').append(msg);