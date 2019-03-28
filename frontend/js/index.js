$('.form').find('input, textarea').on('keyup blur focus', function(e) {

    var $this = $(this),
        label = $this.prev('label');

    if (e.type === 'keyup') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.removeClass('highlight');
        }
    } else if (e.type === 'focus') {

        if ($this.val() === '') {
            label.removeClass('highlight');
        } else if ($this.val() !== '') {
            label.addClass('highlight');
        }
    }

});

$('.tab a').on('click', function(e) {

    e.preventDefault();

    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');

    target = $(this).attr('href');

    $('.tab-content > div').not(target).hide();

    $(target).fadeIn(600);

});

function login() {
    var email = $("#log_email").val();
    var pwd = $("#log_pwd").val();
    //var sha_pwd = hex_sha1(pwd);
    $.ajax({
        type: "post",
        url: "http://192.168.1.185:8080/login",
        cache:false, 
        async:false,
        dataType: "json",
        data: JSON.stringify({ uemail: email, upassword: pwd }),
        success: function(result) {
        	console.log(result);
        	if(result.status!=0){
        		window.location.href="main.html?email="+email;} 
        }
    });
};

function getPosition () {
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (position) {
        let latitude = position.coords.latitude
        let longitude = position.coords.longitude
        let data = {
          latitude: latitude,
          longitude: longitude
        }
        resolve(data)
      }, function () {
        reject(arguments)
      })
    } else {
      reject('你的浏览器不支持当前地理位置信息获取')
    }
  })
}

function signup() {
		getPosition().then(result => {
        // 返回结果示例：
        // {latitude: 30.318030999999998, longitude: 120.05561639999999}
        let queryData = {
          longtitude: String(result.longitude),
          latitude: String(result.latitude),
        }
        // 以下放置获取坐标后你要执行的代码:
        // ...
        var email = $("#email").val();
    	var pwd = $("#pwd").val();
    	var sha_pwd = hex_sha1(pwd);
    	var username = $("#username").val();
    	var state = $("#status").val();
    	console.log(queryData);
	    $.ajax({
	        type: "post",
	        url: "http://192.168.1.185:8080/register",
	        dataType: "text",
	        data: JSON.stringify({ uemail: email, upassword: pwd ,
	         uname : username , ustate : state , ulongi : queryData["longtitude"] ,
	          ulati : queryData["latitude"]}),
	        success: function(result) {
	            alert(result);
	        }
	    });

      }).catch(err => {
        console.log(err)
      })
    
}