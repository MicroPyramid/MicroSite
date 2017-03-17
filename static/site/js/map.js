function win_size(){
  var window_width=$('.map').width()
  //var window_height=$(window).height()-50;
  //var window_size=[window_width,window_height];
  return window_width;
}

function win_size(){
  var window_width=$('.map1').width()
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
    title: 'MicroPyramid'
  });
  /* marker */
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>Hig 499, 6th phase KPHB,<br/> Hyderabad, India - 500072</b></address><a target='_blank' href='https://www.google.co.in/maps/place/MicroPyramid+Informatics+Pvt+Ltd/@17.4857894,78.387813,17z/data=!3m1!4b1!4m2!3m1!1s0x3bcb9144f52b17db:0xa94f62d5a7e9c69a?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
  /* directions */
  var infowindow = new google.maps.InfoWindow({
  content: string_content,
  position:lat_lang_info,

  });
infowindow.open(map);
/* directions */
};



function map_dispaly1() {
  var mapCanvas = document.getElementById('map1');
  var mapOptions = {
    center: new google.maps.LatLng(40.513343, -80.230509),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    
  }
  var map = new google.maps.Map(mapCanvas, mapOptions)
  /* marker */
  var lat_lang={lat:40.513343, lng:-80.230509}
  var lat_lang_info={lat:40.514943, lng:-80.230509}
  var marker = new google.maps.Marker({
    position: lat_lang,
    map: map,
    icon:'/static/site/images/new/map_marker_scaled.png',
    title: 'MicroPyramid'
  });
  /* marker */
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>280 Moon Clinton Rd,<br>STE D Moon Twp, Pittsburgh, Pennsylvania 15108</b></address><a target='_blank' href='https://www.google.co.in/maps/place/280+Moon+Clinton+Rd+d,+Coraopolis,+PA+15108,+USA/@40.5133474,-80.2326973,17z/data=!3m1!4b1!4m5!3m4!1s0x88345da86a70cdd9:0xa2abcb718658d6ad!8m2!3d40.5133433!4d-80.2305086?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
  /* directions */
  var infowindow = new google.maps.InfoWindow({
  content: string_content,
  position:lat_lang_info,

  });
infowindow.open(map);
/* directions */
};

function map_dispaly_uae() {
  var mapCanvas = document.getElementById('map_uae');
  var mapOptions = {
    center: new google.maps.LatLng(25.197197, -55.274376),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    
  }
  var map = new google.maps.Map(mapCanvas, mapOptions)
  /* marker */
  var lat_lang={lat:25.197197, lng:55.274376}
  var lat_lang_info={lat:25.197197, lng:55.274376}
  var marker = new google.maps.Marker({
    position: lat_lang,
    map: map,
    icon:'/static/site/images/new/map_marker_scaled.png',
    title: 'MicroPyramid'
  });
  /* marker */
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>Khalifa Building(Near Old Nesto Super Market),<br>Opp Fire Station, Sharjah, UAE 341246</b></address><a target='_blank' href='https://www.google.co.in/maps/place/280+Moon+Clinton+Rd+d,+Coraopolis,+PA+15108,+USA/@40.5133474,-80.2326973,17z/data=!3m1!4b1!4m5!3m4!1s0x88345da86a70cdd9:0xa2abcb718658d6ad!8m2!3d40.5133433!4d-80.2305086?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
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
  $('.map').css({'width':window_size,'height':'280px'});
}
function initialize1() {
  map_dispaly1();
  var window_size=win_size();
  $('.map1').css({'width':window_size,'height':'280px'});
}
function initialize_uae() {
  map_dispaly_uae();
  var window_size=win_size();
  $('.map_uae').css({'width':window_size,'height':'280px'});
}

$(window).resize(function(e){
  initialize();
})

$(window).resize(function(e){
  initialize1();
})
$(window).resize(function(e){
  initialize_uae();
})
google.maps.event.addDomListener(window, 'load', initialize);
google.maps.event.addDomListener(window, 'load', initialize1);
google.maps.event.addDomListener(window, 'load', initialize_uae);



