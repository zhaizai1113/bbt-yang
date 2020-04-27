const baseURL = "baidu.com";
var request = new XMLHttpRequest();
function getData() {
	let username = $("#username").val();
	let userpass = $("#password").val();
	if (username = '') {
		console.log('用户名不能为空');
	}
	if (userpass = '') {
		console.log('密码不能为空');
	}
	console.log({username,userpass});
	request.open("POST",baseURL + "/post");
	let data = {
		'username': username,
		'userpass': userpass
	}
	Cookies.set('username', username);
	Cookies.set('userpass', userpass)
	console.log(Cookies.get('username'));
	request.send(JSON.stringify(data));
	request.onload = function(e){
		console.log("请求成功");
		console.log({e});
		if (username != '') {
			if(userpass != ''){
				window.location = 'danmu.html';
			}
		}
	}
	request.onerror = function(e){
		console.log("请求失败");
		console.log({e});
	}
}
 function checkUserName(obj){
            var username = obj;
            if(username.trim().length==0){
                  alert("1")
                  obj.focus();
            }
        }
