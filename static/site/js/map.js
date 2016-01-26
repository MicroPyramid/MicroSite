function win_size(){
	var window_width=$('.map').width()
	//var window_height=$(window).height()-50;
	//var window_size=[window_width,window_height];
	return window_width;
}

function map_dispaly() {
  var mapCanvas = document.getElementById('map');
  var mapOptions = {
    center: new google.maps.LatLng(17.485807599999998, 78.3900182),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    
  }
  var map = new google.maps.Map(mapCanvas, mapOptions)
  /* marker */
  var lat_lang={lat:17.485807599999998, lng:78.3900182}
  var lat_lang_info={lat:17.487807599999998, lng:78.3900182}
  var marker = new google.maps.Marker({
    position: lat_lang,
    map: map,
    icon:'/static/site/images/new/map_marker_scaled.png',
    title: 'MicroPyramid Informatics Pvt. Ltd.'
  });
  /* marker */
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>Hig 499, Viswa Sai Dham Appartments,<br>Behind Anupama Hospital, 6th phase<br><b>KPHB, Hyderabad - 72</b></address><a target='_blank' href='https://www.google.co.in/maps/place/MicroPyramid+Informatics+Pvt+Ltd/@17.4857894,78.387813,17z/data=!3m1!4b1!4m2!3m1!1s0x3bcb9144f52b17db:0xa94f62d5a7e9c69a?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
  /* directions */
  var infowindow = new google.maps.InfoWindow({
  content: string_content,
  position:lat_lang_info,

  });
infowindow.open(map);
/* directions */
};



function initialize() {
	map_dispaly();
	var window_size=win_size();
	$('.map').css({'width':window_size,'height':'350px'});
}
$(window).resize(function(e){
  initialize();
})
google.maps.event.addDomListener(window, 'load', initialize);


