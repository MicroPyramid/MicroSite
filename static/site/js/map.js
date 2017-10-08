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
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>Krishe Sapphire, 6th Floor, Madhapur<br/> Hyderabad, India - 500081</b></address><a target='_blank' href='https://www.google.co.in/maps/place/Krishe+Sapphire/@17.4424702,78.3871102,21z/data=!4m8!1m2!2m1!1sKrishe+Sapphire+6th+Floor,+Madhapur!3m4!1s0x0:0xe73625a226ee0c02!8m2!3d17.442418!4d78.3871291?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
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
    center: new google.maps.LatLng(33.0038360, -96.7628019),
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  }
  var map = new google.maps.Map(mapCanvas, mapOptions)
  /* marker */
  var lat_lang={lat:33.0038360, lng:-96.7628019}
  var lat_lang_info={lat:33.0038360, lng:-96.7628019}
  var marker = new google.maps.Marker({
    position: lat_lang,
    map: map,
    icon:'/static/site/images/new/map_marker_scaled.png',
    title: 'MicroPyramid'
  });
  /* marker */
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>3737 Mapleshade Ln, <br>Ste #103, Plano TX 75075, +1 5102300949</b></address><a target='_blank' href='https://www.google.co.in/maps/place/3737+Mapleshade+Ln+%23103,+Plano,+TX+75075,+USA/@33.003836,-96.7649906,17z/data=!3m1!4b1!4m5!3m4!1s0x864c2213cb53d0c7:0x9dc1659b19dd01c9!8m2!3d33.003836!4d-96.7628019?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
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
  var string_content="<div class='map_address'><br><img src='/static/site/images/new/company_logo.gif'><br><br><address>Sharjah, UAE 341246</b></address><a target='_blank' href='https://www.google.co.in/maps/place/Burj+Khalifa/@25.197197,55.2721877,17z/data=!3m1!4b1!4m5!3m4!1s0x3e5f43348a67e24b:0xff45e502e1ceb7e2!8m2!3d25.197197!4d55.2743764?hl=en'><img src='/static/site/images/new/dirextions_link.png'></a></div>"
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



