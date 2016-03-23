var cv = require('opencv');
var path = require('path');

// When opening a file, the full path must be passed to opencv
var vid = new cv.VideoCapture(0);
var window = new cv.NamedWindow('Video', 0);

vid.read(function(err, mat){
  if (err) throw err;

  var midx = mat.size()[1] / 2;
  var midy = mat.size()[0] / 2;
  var size = 50;
  var rect = [midx - size/2, midy - size/2, midx + size/2, midy + size/2];
  console.log(midx, midy);
  console.log(rect);
  var track = new cv.TrackedObject(mat, rect, {channel: 'value'});
  var x = 0;
  var iter = function(){
    vid.read(function(err, m2){
      var rec = track.track(m2)
      console.log('>>', x, ':' , rec)
      m2.rectangle([rec[0], rec[1]], [rec[2], rec[3]])
      m2.rectangle([midx - size/2, midy - size/2], [size, size])
      window.show(m2);
      window.blockingWaitKey(0, 50);
      iter();
    })
  }
  iter();
})













/*try {
  var camera = new cv.VideoCapture(0);
  var window = new cv.NamedWindow('Video', 0)
} catch (e){
  console.log("Couldn't start camera:", e)
}

render_frame();

function render_frame() {
  camera.read(function(err, im) {
    if (err) throw err;

    im.detectObject(cv.FACE_CASCADE, {}, function(err, faces){
      for (var i=0;i<faces.length; i++){
        var x = faces[i]
        im.ellipse(x.x + x.width/2, x.y + x.height/2, x.width/2, x.height/2);
      }
      if (im.size()[0] > 0 && im.size()[1] > 0){
        window.show(im);
      }
      window.blockingWaitKey(0, 50);
      setTimeout(render_frame, 1);
    });
  });
}*/