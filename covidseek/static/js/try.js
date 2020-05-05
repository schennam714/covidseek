<script>
  var map;
  function initialize() {
    var center = new google.maps.LatLng(38.9696, -77.3861);
    map = new google.maps.Map(document.getElementById("map"), {
      center: center,
      zoom: 13,
    });
  }
  google.maps.event.addDomListener(window, "load", initialize);
</script>