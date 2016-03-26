
var container, stats;

var camera, scene, renderer;

var cube, xaxis, yaxis, zaxis;

var targetRotation = 0;
var targetRotationOnMouseDown = 0;

var windowHalfX = window.innerWidth / 2;
var windowHalfY = window.innerHeight / 2;

var poseMatrix = null;

function makeTranslationMatrix(x, y, z) {
  var m = new THREE.Matrix4();
  m.set(
    1, 0, 0, x,
    0, 1, 0, y,
    0, 0, 1, z,
    0, 0, 0, 1);
  return m;
}

$(document).ready(function() {
  var fixer = new THREE.Matrix4();
  fixer.set(
    1,  0,  0, 0,
    0,  1,  0, 0,
    0,  0,  1, 0,
    0,  0,  0, 1);
  var x = 0;
  var updater = function() {
    $.get("/debug/getinfo/", {}, function(data) {
      if (data != "") {
        var parsed = JSON.parse(data);
        var mtx = parsed["matrix"];
        var pose = parsed["pose"];
        var pmtx = new THREE.Matrix4();
        x++;
        if (x == 10)
          poseMatrix = mtx;
        if (poseMatrix) {
          pmtx.set(poseMatrix[1], poseMatrix[4], poseMatrix[7], 0,
                   poseMatrix[2], poseMatrix[5], poseMatrix[8], 0,
                   poseMatrix[0], poseMatrix[3], poseMatrix[6], 0,
                               0,             0,             0, 1);
        }
        if (mtx) {
          var m = new THREE.Matrix4();
          m.set(mtx[1], mtx[4], mtx[7], 0,
                mtx[2], mtx[5], mtx[8], 0,
                mtx[0], mtx[3], mtx[6], 0,
                     0,      0,      0, 1);
          var mI = new THREE.Matrix4();
          mI.getInverse(m);
          pmtx.multiply(mI);
          var final = new THREE.Matrix4();
          final.multiply(fixer).multiply(pmtx);
          cube.matrix = final;
          cube.matrixAutoUpdate = false;

          xaxis.matrix = final;
          xaxis.matrixAutoUpdate = false;
          yaxis.matrix = final;
          yaxis.matrixAutoUpdate = false;
          zaxis.matrix = final;
          zaxis.matrixAutoUpdate = false;
        }
      }
    });
  }

  setInterval(updater, 100);

  init();
  animate();

  function init() {
    container = document.createElement( 'div' );
    document.body.appendChild( container );

    camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 2000 );
    camera.position.y = 0;
    camera.position.z = -1000;

    scene = new THREE.Scene();

    // Cube

    var geometry = new THREE.BoxGeometry( 200, 200, 200 );

    for ( var i = 0; i < geometry.faces.length; i += 2 ) {
      var hex = Math.random() * 0xffffff;
      geometry.faces[ i ].color.setHex( hex );
      geometry.faces[ i + 1 ].color.setHex( hex );
    }

    var material = new THREE.MeshBasicMaterial( { vertexColors: THREE.FaceColors, overdraw: 0.5 } );

    cube = new THREE.Mesh( geometry, material );
    scene.add( cube );
    camera.lookAt(cube.position);

    var xgeometry = new THREE.BoxGeometry(300, 20, 20);
    xgeometry.translate(150, 0, 0);
    var ygeometry = new THREE.BoxGeometry(20, 300, 20);
    ygeometry.translate(0, 150, 0);
    var zgeometry = new THREE.BoxGeometry(20, 20, 300);
    zgeometry.translate(0, 0, 150);
    xaxis = new THREE.Mesh(xgeometry, new THREE.MeshBasicMaterial({color: 0xff0000}));
    scene.add(xaxis);
    yaxis = new THREE.Mesh(ygeometry, new THREE.MeshBasicMaterial({color: 0x00ff00}));
    scene.add(yaxis);
    zaxis = new THREE.Mesh(zgeometry, new THREE.MeshBasicMaterial({color: 0x0000ff}));
    scene.add(zaxis);

    renderer = new THREE.CanvasRenderer();
    renderer.setClearColor( 0xf0f0f0 );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( window.innerWidth, window.innerHeight );
    container.appendChild( renderer.domElement );

    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '0px';
    container.appendChild( stats.domElement );

    window.addEventListener( 'resize', onWindowResize, false );
  }

  function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );
  }

  function animate() {
    requestAnimationFrame( animate );

    stats.begin();
    render();
    stats.end();
  }

  function render() {
    cube.rotation.y += ( targetRotation - cube.rotation.y ) * 0.05;
    renderer.render( scene, camera );
  }
});
