$(document).ready(function() {
  var updater = function() {
    $.get("/debug/getinfo/", {}, function(data) {
      if (data != "") {
        var parsed = JSON.parse(data);
        var mtx = parsed["matrix"];
        console.log(mtx);
      }
    });
  }

  setInterval(updater, 500);
});