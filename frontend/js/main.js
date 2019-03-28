function initMap() {
        var newyork = {lat: 40.711328,  lng: -73.997250};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 13,
          center: newyork
        });
        var styles = [{"featureType": "landscape", 
        "stylers": [{"saturation": -100}, {"lightness": 65}, {"visibility": "on"}]},
                   {"featureType": "poi", "stylers": [{"saturation": -100}, {"lightness": 51}, {"visibility": "simplified"}]},
                    {"featureType": "road.highway", "stylers": [{"saturation": -100}, {"visibility": "simplified"}]}, 
                    {"featureType": "road.arterial", "stylers": [{"saturation": -100}, {"lightness": 30}, {"visibility": "on"}]}, 
                    {"featureType": "road.local", "stylers": [{"saturation": -100}, {"lightness": 40}, {"visibility": "on"}]},
                     {"featureType": "transit", "stylers": [{"saturation": -100}, {"visibility": "simplified"}]}, 
                     {"featureType": "administrative.province", "stylers": [{"visibility": "off"}]}, 
                     {"featureType": "water", "elementType": "labels", "stylers": [{"visibility": "on"},
                      {"lightness": -25}, {"saturation": -100}]}, 
                      {"featureType": "water", "elementType": "geometry", "stylers": [{"hue": "#ffff00"}, {"lightness": -25}, {"saturation": -97}]}];
        map.set('styles', styles);
        var curlocation = new google.maps.Marker({
          position: newyork,
          map: map,
          draggable: true
        });

        (function(marker){
          var infowindow = new google.maps.InfoWindow({
            maxWidth:200,
            content:"Current Location"
          });
          marker.addListener('click',function(){
            infowindow.open(map,marker);
          });
          marker.addListener('dragend',function(evt){
            document.getElementById("lat").value = evt.latLng.lat();
            document.getElementById("log").value = evt.latLng.lng();
          })
        })(curlocation);


        $.ajax({
        type: "post",
        url: "http://192.168.1.185:8080/notes/timeline",
        cache:false, 
        async:false,
        dataType: "json",
        data: JSON.stringify({ uemail: email}),
        success: function(result) {
          var markers = new Array();
          var infowindows = new Array();
          console.log(result);
          for (let i=0,len = result.notesList.length;i<len;i++){
            // console.log(result.notesList[i]);
            markers[i] = new google.maps.Marker({
              position:{lat:Number(result.notesList[i].nlati),lng:Number(result.notesList[i].nlongi)},
              map: map,
              title: result.notesList[i].ntime
            });
            var tagstring = '';
            for (tag in result.notesList[i].tag){
              tagstring = tagstring+tag;
            }
            uid = result.notesList[i].uid;
            var contentstring = '<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h3 id="firstHeading" class="firstHeading">'+'From User:'+'<a href="profile.html?email='+email+'&uid='+uid+'">'+result.notesList[i].username+'</a></h3>'+
            '<div id="bodyContent">'+
            '<p>tags:'+result.notesList[i].tag+'</p>'+
            '<br>'+
            '<p>'+result.notesList[i].ntext+'</p>';
            if(result.notesList[i].commentable=="1"){
              contentstring+='<input type="text" name="comment" id="newcomment" value="Your Comment">'+
              '<br>'+
              '<input type="button" value="Submit" onclick="makecomment('+result.notesList[i].nid+')">'+
              '<input type="button" value="See all comments" onclick="window.location.href=&apos;comments.html?nid='
              +result.notesList[i].nid+'&email='+email+'&apos;">'
            }

            infowindows[i] = new google.maps.InfoWindow({
              content: contentstring,
              maxWidth: 200
            });

            markers[i].addListener('click', function() {
              infowindows[i].open(map, markers[i]);
            });

            }//for loop
          }//Success
      });//Ajax
};

function makecomment(noteid){
  var comment = $("#newcomment").val();
  $.ajax({
        type: "post",
        url: "http://192.168.1.185:8080/notes/"+noteid.toString()+"/comment",
        dataType: "json",
        data: JSON.stringify({ uemail: email, ctext: comment}),
        success: function(result) {
          if (result.status==1) {alert("Comment Submit Success.")}
          else{alert("Comment Submit Failed.")}
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

function getlocation() {
    getPosition().then(result => {
        // 返回结果示例：
        // {latitude: 30.318030999999998, longitude: 120.05561639999999}
        let queryData = {
          latitude: String(result.latitude),
          longtitude: String(result.longitude),
        }
        // 以下放置获取坐标后你要执行的代码:
        // ...
      $('#lat').attr("value",queryData["latitude"])
      $('#log').attr("value",queryData["longtitude"])
      // $.ajax({
      //   type: "post",
      //   url: "http://192.168.1.185:8080/updateUserLocation",
      //   cache:false, 
      //   async:false,
      //   dataType: "json",
      //   data: JSON.stringify({ uemail: email, ulati : queryData["latitude"], ulongi : queryData["longtitude"]  }),
      //   success: function(result) {
      //       console.log("Location updated")
      //     }
      // });
      }).catch(err => {
        console.log(err)
      })
    
}
Date.prototype.Format = function (fmt) { // author: meizz
        var o = {
            "M+": this.getMonth() + 1, // 月份
            "d+": this.getDate(), // 日
            "h+": this.getHours(), // 小时
            "m+": this.getMinutes(), // 分
            "s+": this.getSeconds(), // 秒
            "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
            "S": this.getMilliseconds() // 毫秒
        };
        if (/(y+)/.test(fmt))
            fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                return fmt;
    }

function refreshlocation(){
    var latitude = $("#lat").val();
    var longtitude = $("#log").val();
    var ctime = $("#ctime").val();
    alert("refreshed");
    $.ajax({
        type: "post",
        url: "http://192.168.1.185:8080/updateUserLocation",
        dataType: "text",
        data: JSON.stringify({ uemail: email, ulongi : longtitude, ulati : latitude, ucurrentTime : ctime}),
        success: function(result) {
            window.location.href="main.html?email="+email; 
        }
    });
}

function logout(){
  alert("logout");
  $.ajax({
        type: "post",
        url: "http://192.168.1.185:8080/logout",
        dataType: "text",
        data: JSON.stringify({ uemail: email}),
        success: function(result) {
            window.location.href="index.html"; 
        }
    });
}