$(document).ready(function(){
  let namespace = "/test";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');

  var localMediaStream = null;

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 300, 150);

    let dataURL = canvas.toDataURL('image/jpeg');
    socket.emit('input image', dataURL);
  }

  socket.on('connect', function() {
    console.log('Connected!');
    const sessionID = socket.id;
    console.log(sessionID)
    var imageElement = document.getElementById("imageElement");
    var userID = sessionID.replace("/test#", "")
    console.log(userID);
    
    var tempp = '/video_feed/'.concat(userID);
    console.log(tempp);  
    console.log(imageElement.src);
    imageElement.src = (imageElement.src).concat(tempp)
    console.log(imageElement.src);
  });

  var constraints = {
    video: {
      width: { min: 640 },
      height: { min: 480 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;

    setInterval(function () {
      sendSnapshot();
    }, 500);
  }).catch(function(error) {
    console.log(error);
  });
});

