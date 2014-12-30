var $ = jQuery;

/* ---  exists  ----- */
jQuery.fn.exists = function() {
  return $(this).length;
};

/* ----------------------- Load img with http://placehold.it/-----------------*/

// jQuery(window).load(function() {
//   var $ = jQuery;
  
//   $('img:not(".logo-img")').each(function() {
//   if (/MSIE (\d+\.\d+);/.test(navigator.userAgent)){
//     var ieversion=new Number(RegExp.$1)
//     if (ieversion>=9)
//     if (typeof this.naturalWidth === "undefined" || this.naturalWidth === 0) {
//       this.src = "http://placehold.it/" + ($(this).attr('width') || this.width || $(this).naturalWidth()) + "x" + (this.naturalHeight || $(this).attr('height') || $(this).height());
//     }
//   } else {
//     if (!this.complete || typeof this.naturalWidth === "undefined" || this.naturalWidth === 0) {
//     this.src = "http://placehold.it/" + ($(this).attr('width') || this.width) + "x" + ($(this).attr('height') || $(this).height());
//     }
//   }
//   });
// });

/* ------------------------ Preloader ------------------------- */
jQuery(document).ready(function($) {  
  // site preloader -- also uncomment the div in the header and the css style for .preloader
  $(window).load(function(){
    $('.preloader').fadeOut('slow',function(){$(this).remove();});
  });
});


/* ----------------------- Add class Touch device ------------------------ */
if( navigator.userAgent.match(/iPad|iPhone|Android/i) ) {
	$('body').addClass('touch-device');
}
else{
  $('body').addClass('no-touch-device');
}


/* ------------------- height first slider ---------------------*/

if($(".first-page, .royalSlider").exists()) {
  $(document).ready(function() { 
    $('.first-page, .royalSlider').css('height', window.innerHeight);
  });

  $(window).resize(function() {
    $('.first-page, .royalSlider').css('height', $(window).height());
  });
}


/* ----------------- open menu slide -------------------- */
$(document).ready(function() {
  $("#menu-open").click(function() {  
		if ($("#wrapper, #slide-menu, #wrapper-header").hasClass("open-menu")) {
			$("#wrapper, #slide-menu, #wrapper-header").removeClass("open-menu");   
		}
		else {
			$("#wrapper, #slide-menu, #wrapper-header").addClass("open-menu");     
		}
	});
  $(".menu-close, #wrapper").click(function() {  
		$("#wrapper, #slide-menu, #wrapper-header").removeClass("open-menu");   
	});
});




/* --------------------- open second ul menu slide ------------------- */

$(document).ready(function() {                     
  $( "#navigation-menu li.collapsed" ).click(function() {
    $( this ).toggleClass( "start-collapsed" );
  });
});


$(document).ready(function() {
  var url = window.location.pathname, 
      urlRegExp = new RegExp(url.replace(/\/$/,'') + "$"); // create regexp to match current url pathname and remove trailing slash if present as it could collide with the link in navigation in case trailing slash wasn't present there
	
	// now grab every link from the navigation
	$('#navigation-menu a').each(function(){
			// and test its normalized href against the url pathname regexp
			if(urlRegExp.test(this.href.replace(/\/$/,''))){
				$(this).addClass('active');
			}
	});
});



/* ---------------------------- STYLED SELECT  ----------------------- */
$(document).ready(function(){
  if($("select").size()){
  $(function() {  
    $('select').styler();  
    });
  }
});

/* ------------ add class fixed for menu -------------- */
$(document).ready(function(){
		$(window).bind('scroll', function() {
		var navHeight = $( window ).height() - 100;
			if ($(window).scrollTop() > navHeight) {
				$('#wrapper-header').addClass('fixed');
			}
			else {
				$('#wrapper-header').removeClass('fixed');
			}
	 });
 });

/* ---------------------------- SCROLL TOP and ather files ----------------------- */
$(document).ready(function() {  
  $('.my-scroll').on('click', function(e) {
    e.preventDefault();
    var $link = $(this).attr('href');
    
    $('html, body').animate({
      scrollTop: $($link).offset().top - 0
    }, 800 );
  });
});
   

/* ---------------------------- SCROLL to object----------------------- */
$(document).ready(function() {  
  $('.p-scroll').on('click', function(e) {
    e.preventDefault();
    var $link = $(this).attr('href');
    
    $('html, body').animate({
      scrollTop: $($link).offset().top - (-70)
    }, 800 );
  });
});


/* ---------------------------- CaruFredSel  ----------------------- */
$(window).load(function() {
	if($(".foo3").exists()) {
		$('.foo3').carouFredSel({
		responsive: true,
			width: '100%',
			prev: '.prev3',
			next: '.next3',
			scroll: {
				items: 1,
				speed: 500,
				timeoutDuration:300000
			},
			items: {
				width:900,
				height: 'auto',  //  optionally resize item-height
				visible: {
					min: 1,
					max: 1
				}
			},
			onCreate: function(){ 
				$(this).addClass('init');
				$(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
				setTimeout(function() {
					$(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
				}, 500);
			},
			swipe       : {
				onTouch     : false,
				onMouse     : false
			}

		})
		.removeClass('load')
		.touchwipe({
			wipeLeft: function() {
				$('.foo3').trigger('next', 1);
			},
			wipeRight: function() {
				$('.foo3').trigger('prev', 1);
			},
			preventDefaultEvents: false
		});
	}

	 if($(".foo7").exists()) {
			$('.foo7').carouFredSel({
			responsive: true,
			width: '100%',
			prev: '.prev7',
			next: '.next7',
			scroll: {
				items: 1,
				speed: 500,
				timeoutDuration:300000
			},
			items: {
				width: 780,
				height: 'auto',  //  optionally resize item-height
				visible: {
					min: 1,
					max: 1
				}
			},
			onCreate: function(){
				$(this).addClass('init');
				$(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
				setTimeout(function() {
					$(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
				}, 500);
			}

		})
		.removeClass('load')
		.touchwipe({
			wipeLeft: function() {
				$('.foo7').trigger('next', 1);
			},
			wipeRight: function() {
				$('.foo7').trigger('prev', 1);
			},
			preventDefaultEvents: false
		});
	}
});


/* ---------------------------- ISOTOP  ----------------------- */
$(document).ready(function() {  
  if($(".isotope").exists()) {
    // initialize Isotope after all images have loaded
    var $container = $('.isotope').imagesLoaded( function() {
      $container.isotope({
        itemSelector: '.element-item',
        layoutMode: 'fitRows'
      });
    });
      
    // filter functions
    var itemReveal = Isotope.Item.prototype.reveal;
    Isotope.Item.prototype.reveal = function() {
      itemReveal.apply( this, arguments );
      $( this.element ).removeClass('isotope-hidden');
    };
  
    var itemHide = Isotope.Item.prototype.hide;
    Isotope.Item.prototype.hide = function() {
      itemHide.apply( this, arguments );
      $( this.element ).addClass('isotope-hidden');
    };
    
    // demo code
    $( function() {
      var $container = $('.isotope');
      $container.isotope({
        layoutMode: 'fitRows'
      });
      $('#filters').on( 'click', 'button', function() {
        var filtr = $( this ).attr('data-filter');
        $container.isotope({ filter: filtr });
      });
    });

    // change is-checked class on buttons
    $('.button-group').each( function( i, buttonGroup ) {
      var $buttonGroup = $( buttonGroup );
      $buttonGroup.on( 'click', 'button', function() {
        $buttonGroup.find('.is-checked').removeClass('is-checked');
        $( this ).addClass('is-checked');
      });
    });

  }

  animations();

});


/* ---------------------------- GOOGLE MAPS  ----------------------- */
/* --- map for md device ---- */
if($("#map-canvas-lg").exists()) {
  $(document).ready(function() {  
    function initialize() {
      var mapOptions = {
        zoom: 10,
        draggable: false,
        scrollwheel: false,
        center: new google.maps.LatLng(40.8, -74.5)
      },
      map = new google.maps.Map(document.getElementById('map-canvas-lg'), mapOptions);

      var image = 'images/marker.png';
      var myLatLng = new google.maps.LatLng(40.756168, -73.978705);
      var beachMarker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon: image,
          title: 'Manhattan'
      });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
    google.maps.event.addDomListener(window, 'resize', initialize);
  });
}

/* --- map for sm device --- */
if($("#map-canvas-sm").exists()) {
  $(document).ready(function() {  
    function initialize() {
      var mapOptions = {
        zoom: 10,
        draggable: false,
        scrollwheel: false,
        center: new google.maps.LatLng(40.8, -74.5)
      },
      map = new google.maps.Map(document.getElementById('map-canvas-sm'), mapOptions);

      var image = 'images/marker.png';
      var myLatLng = new google.maps.LatLng(40.756168, -74.178705);
      var beachMarker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon: image,
          title: 'Manhattan'
      });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
    google.maps.event.addDomListener(window, 'resize', initialize);
  });
}

/* ---  map for sm device --- */

if($("#map-canvas-xs").exists()) {
  $(document).ready(function() {  
    function initialize() {
      var mapOptions = {
        zoom: 10,
        draggable: false,
        scrollwheel: false, 
        center: new google.maps.LatLng(41.2, -73.98)
      },
      map = new google.maps.Map(document.getElementById('map-canvas-xs'), mapOptions);

      var image = 'images/marker.png';
      var myLatLng = new google.maps.LatLng(40.756168, -73.978705);
      var beachMarker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon: image,
          title: 'Manhattan'
      });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
    google.maps.event.addDomListener(window, 'resize', initialize);
  });

}

/* ----------------------- Accordion --------------------------- */
$(document).ready(function() {  
  function toggleChevron(e) {
		$(e.target)
			.prev('.panel-heading')
			.find("i.indicator")
			.toggleClass('glyphicon-minus glyphicon-plus');
  }
  $('.accordion').on('hidden.bs.collapse', toggleChevron);
  $('.accordion').on('shown.bs.collapse', toggleChevron);
});


/*-------------------------------- myTab -------------------------*/
$(document).ready(function() {
  if($(".myTab").size()){
    $('.myTab').tabCollapse();
  }
});


/*-------------------------------- Fancy box -------------------------*/
$(document).ready(function() {
  if($(".fancybox").size()){
    $(".fancybox").fancybox({
      openEffect : 'none',
      closeEffect : 'none'
    });
  }
});

/* ----------------------------- Royal slider ----------------------- */
if($("#full-width-slider").exists()) {
  $(document).ready(function() { 
		$('#full-width-slider').royalSlider({
			imageScaleMode: 'fill',
			transitionType: 'fade',
			keyboardNavEnabled: true,
			controlNavigation: 'bullets',
			arrowsNav: false,
			autoPlay: {
				enabled: true,
				delay: 5000
			}
		});
  });
}


/* Demo 2 */
jQuery(document).ready(function($) {
  jQuery.rsCSS3Easing.easeOutBack = 'cubic-bezier(0.175, 0.885, 0.320, 1.275)';
  $('#slider-with-blocks-1').royalSlider({
    arrowsNav: true,
    arrowsNavAutoHide: false,
    fadeinLoadedSlide: false,
    controlNavigationSpacing: 0,
    controlNavigation: 'bullets',
    blockLoop: true,
    loop: true,
    numImagesToPreload: 6,
    transitionType: 'fade',
    keyboardNavEnabled: true,
    autoScaleSlider: true, 
    block: {
      delay: 400
    },
    imageScaleMode: 'fill',
    imageAlignCenter: true,
  });
});


/* -------------------------------------- SOCIAL BUTTONS ---------------------------------------*/
function socialLink(){
	var urlsoc = location.href;

  // TWITTER SHARE
  new GetShare({
    root: $('.gt-tw'),
    network: "twitter",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+' '
    }
  });

  // LINKEDIN SHARE
  new GetShare({
      root: $('.gt-in'),
    network: "linkedin",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+' '
    }
  });

  // VK SHARE
  new GetShare({
      root: $('.gt-vk'),
    network: "vk",
    button: {text: ""},
    share: {
      url: urlsoc
    }
  });

  // STUMBLEUPON SHARE
  new GetShare({
      root: $('.gt-st'),
    network: "stumbleupon",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+''
    }
  });

  // FACEBOOK SHARE
  new GetShare({
    root: $('.gt-fb'),
    network: "facebook",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+' '
    }
   });

  // GOOGLE+ SHARE
  new GetShare({
    root: $('.gt-gp'),
    network: "googleplus",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+' '
    }
   });

  // PINTEREST SHARE
  new GetShare({
    root: $('.gt-pt'),
    network: "pinterest",
    button: {text: ""},
    share: {
      url: urlsoc,
      message: 'Link to '+urlsoc+' '
    }
  });
}

if($(".social-inp").exists()) {
	socialLink();
}


/* --------- shareCount -------------- */
function shareCount() {
  var numb = $('.post-soc-icon .social-inp .getshare-counter'),
    allCount = 0;
  numb.each(function () {
    allCount = allCount + Number($(this).html());
  });
  $('.count-shared .quantity').html(allCount);
}
setTimeout(function() {
  shareCount();
  setTimeout(function() {
    shareCount();
  }, 2000);
}, 1000);


/*---------------------------------- Circules -------------------------------------*/

/* skill-85 */
if($('.skill-85 canvas').exists()){
  var skill = $('.skill-85 canvas');

  skill.each(function(){
    var $this = $(this),
        color = '#000',
        startcolorline = '#f2f2f2',
        title;
    
    if ($this.attr('data-color') !== undefined &&  $this.attr('data-color') !== false)
      color = $this.attr('data-color');
      
    if ($this.attr('data-start-color') !== undefined &&  $this.attr('data-start-color') !== false)
      startcolorline = $this.attr('data-start-color');
      
    title = $this.text();

		$this.appear(function() {
			$this.easyCircleSkill({
				percent        : 85,
				linesize       : 3,
				startcolorline : startcolorline,
				skillName      : title,
				colorline      : color
			});
		});
  });
}


/* skill-55 */
if($('.skill-55 canvas').exists()){
  var skill = $('.skill-55 canvas');
  
  skill.each(function(){
    var $this = $(this),
        color = '#000',
        startcolorline = '#f2f2f2',
        title;
    
    if ($this.attr('data-color') !== undefined &&  $this.attr('data-color') !== false)
      color = $this.attr('data-color');
      
    if ($this.attr('data-start-color') !== undefined &&  $this.attr('data-start-color') !== false)
      startcolorline = $this.attr('data-start-color');
      
    title = $this.text();
    
		$this.appear(function() {
			$this.easyCircleSkill({
				percent        : 55,
				linesize       : 3,
				startcolorline : startcolorline,
				skillName      : title,
				colorline      : color
			});
		});
  });
}

/* skill-73 */
if($('.skill-73 canvas').exists()){
  var skill = $('.skill-73 canvas');
  
  skill.each(function(){
    var $this = $(this),
        color = '#000',
        startcolorline = '#f2f2f2',
        title;
    
    if ($this.attr('data-color') !== undefined &&  $this.attr('data-color') !== false)
      color = $this.attr('data-color');
      
    if ($this.attr('data-start-color') !== undefined &&  $this.attr('data-start-color') !== false)
      startcolorline = $this.attr('data-start-color');
      
    title = $this.text();
    
		$this.appear(function() {
			$this.easyCircleSkill({
				percent        : 73,
				linesize       : 3,
				startcolorline : startcolorline,
				skillName      : title,
				colorline      : color
			});
		});
  });
}

/* skill-48 */
if($('.skill-48 canvas').exists()){
	var skill = $('.skill-48 canvas');
	
	skill.each(function(){
		var $this = $(this),
				color = '#000',
				startcolorline = '#f2f2f2',
				title;
		
		if ($this.attr('data-color') !== undefined &&  $this.attr('data-color') !== false)
			color = $this.attr('data-color');
			
		if ($this.attr('data-start-color') !== undefined &&  $this.attr('data-start-color') !== false)
			startcolorline = $this.attr('data-start-color');
			
		title = $this.text();
		
		$this.appear(function() {
			$this.easyCircleSkill({
				percent        : 48,
				linesize       : 3,
				startcolorline : startcolorline,
				skillName      : title,
				colorline      : color
			});
		});
	});
}


/* ----------------------- nav slider foo1, foo2 --------------------------*/

/* foo2*/
// if($(".slider-foo-2 a.prev, .slider-foo-2 a.next").exists()) {
//   $(document).ready(function() { 
//     $('.slider-foo-2 a.prev, .slider-foo-2 a.next').css("top",  Math.floor($('.foo2 .img-block img').height()/2) );
//     setTimeout(function() {
//       $('.slider-foo-2 a.prev, .slider-foo-2 a.next').css("top",  Math.floor($('.foo2 .img-block img').height()/2));
//     }, 1000);
//   });


//   $(window).resize(function() {
//     $('.slider-foo-2 a.prev, .slider-foo-2 a.next').css("top",  Math.floor($('.foo2 .img-block img').height()/2) );
//   });

// }


/* ---------------------- Close Portfolio slider ------------------------- */
// $("#filters button").click(function() {
//   $('.sliders .container').hide();
//   destroy('#albom');
//   $(".sliders").css('min-height', 0);
  
// });


/* -------------------------- Remove Video ---------------------------*/
if( navigator.userAgent.match(/iPad|iPhone|Android/i) ) {
  jQuery('.bg-video, .header-video').find('video').remove();
}


/* -------------------------------- RETINA ---------------------------*/
if( 'devicePixelRatio' in window && window.devicePixelRatio == 2 ){
	var imgToReplace = $('img.replace-2x').get();
 
	for (var i=0,l=imgToReplace.length; i<l; i++) {
		var src = imgToReplace[i].src;
		src = src.replace(/\.(png|jpg|gif)+$/i, '@2x.$1');
		imgToReplace[i].src = src;
	 
		$(imgToReplace[i]).load(function(){
			$(this).addClass('loaded');
		});
	}
}


/* --------------------------- Background Clip Title ------------------------------ */
function titleParams() {
  var title = $('.title-box .title'),
      padding = $('.slider-overlay .bg-padding');
  
  if (title.attr('data-fontsize') !== undefined && title.attr('data-fontsize') !== false && title.attr('data-fontsize') !== '') {
    var fontSize = title.attr('data-fontsize');
    
    title.css('fontSize', fontSize + 'px');
    padding.css('height', fontSize * 0.16);
    
    if ($('body').width() < 992 && $('body').width() > 767) {
      title.css('fontSize', (fontSize * 0.57) + 'px');
      padding.css('height', fontSize * 0.57 * 0.16);
    } else if ($('body').width() < 768) {
      title.css('fontSize', (fontSize * 0.25) + 'px');
      padding.css('height', fontSize * 0.25 * 0.16);
    }
  }
  
  if (title.attr('data-fontweight') !== undefined && title.attr('data-fontweight') !== false && title.attr('data-fontweight') !== '') {
    title.css('fontWeight', title.attr('data-fontweight'));
  }
  
  if (title.attr('data-fontfamily') !== undefined && title.attr('data-fontfamily') !== false && title.attr('data-fontfamily') !== '') {
    title.css('fontFamily', title.attr('data-fontfamily'));
  }
  
  if (title.attr('data-bg') !== undefined && title.attr('data-bg') !== false && title.attr('data-bg') !== '') {
    $('.slider-overlay .slider-content .bg').css('background', title.attr('data-bg'));
  }
}

function titleCanvas() {
  var titleBox    = $('.title-box'),
      title       = titleBox.find('.title'),
      titleWidth  = title.width(),
      titleHeight = title.height(),
      fontSize    = 190,
      fontWeight  = 800,
      fontFamily  = '"Raleway", sans-serif',
      bg          = 'rgba(255, 255, 255, 0.85)';
    
  fontSize = parseFloat(title.css('font-size'));
  
  if (title.attr('data-fontweight') !== undefined && title.attr('data-fontweight') !== false && title.attr('data-fontweight') !== '') {
    fontWeight =  parseFloat(title.attr('data-fontweight'));
  }
  
  if (title.attr('data-fontfamily') !== undefined && title.attr('data-fontfamily') !== false && title.attr('data-fontfamily') !== '') {
    fontFamily = title.attr('data-fontfamily');
  }
  
  if (title.attr('data-bg') !== undefined && title.attr('data-bg') !== false && title.attr('data-bg') !== '') {
    bg = title.attr('data-bg');
  }

  function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  var words = text.split(' ');
  var line = '';

  for(var n = 0; n < words.length; n++) {
    var testLine = line + words[n] + '';
    var metrics = ctx.measureText(testLine);
    var testWidth = metrics.width;
    if (testWidth > maxWidth && n > 0) {
      ctx.fillText(line, x, y);
      line = words[n] + '';
      y += lineHeight;
    }
    else {
      line = testLine;
    }
  }
  ctx.fillText(line, x, y);
  }
  $('.title-canvas').remove();
  
  titleBox.find('.title').after('<canvas class="title-canvas" width="' + titleWidth + '" height="' + titleHeight + '"></canvas>');
  
  var canvas = titleBox.find('.title-canvas').get(0),
    ctx = canvas.getContext("2d");

  ctx.fillStyle = bg; 
  ctx.fillRect(0,0,titleWidth,titleHeight);
  
  ctx.font = fontWeight + ' ' + fontSize + 'px ' + fontFamily;
  ctx.fillStyle = '#333';
  ctx.textAlign = 'center';

  ctx.globalCompositeOperation = 'destination-out';
  wrapText(ctx, title.text(), titleWidth / 2 , fontSize * 0.87, titleWidth, fontSize);
  title.addClass('hidden-title');
  titleBox.closest('.slider-overlay').addClass('loaded');
}

function carousels() {
  if($(".foo1").exists()) {
    $('.foo1').carouFredSel({
      responsive: true,
      width: '100%',
      prev: '.prev1',
      next: '.next1',
      scroll: {
        items: 1,
        speed: 500,
        timeoutDuration:300000},
     
      items: {
        width: 350,
        height: 'auto',  //  optionally resize item-height
        visible: {
          min: 1,
          max: 3
        }
      },
      onCreate: function(){ 
        $(this).addClass('init');
        $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        setTimeout(function() {
          $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        }, 500);
        
        var top = $(this).find('.img-block img').height();
        $(this).closest('.post-slider').find('.prev, .next').css('top', top / 2);
      }
    }).touchwipe({
      wipeLeft: function() {
        $('.foo1').trigger('next', 1);
      },
      wipeRight: function() {
        $('.foo1').trigger('prev', 1);
      },
			preventDefaultEvents: false
    });
  }
  
  if($(".foo2").exists()) {
      $('.foo2').carouFredSel({
      responsive: true,
      width: '100%',
      prev: '.prev2',
      next: '.next2',
      scroll: {
        items: 1,
        speed: 500,
        timeoutDuration:300000},
     
      items: {
        width: 1170,
        height: 'auto',
        visible: {
          min: 1,
          max: 1
        }
      },
      onCreate: function(){ 
        $(this).addClass('init');
        $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        setTimeout(function() {
          $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        }, 500);
        
        var top = $(this).find('.img-block img').height();
        $(this).closest('.slider-foo-2').find('.prev, .next').css('top', top / 2);
      }
    }).touchwipe({
      wipeLeft: function() {
        $('.foo2').trigger('next', 1);
      },
      wipeRight: function() {
        $('.foo2').trigger('prev', 1);
      },
			preventDefaultEvents: false
    });
  }

  if($(".foo4").exists()) {
    $('.foo4').carouFredSel({
      responsive: true,
      width: '100%',
      prev: '.prev4',
      next: '.next4',
      scroll: {
        items: 1,
        speed: 500,
        timeoutDuration:300000
      },
      items: {
        visible: {
          min: 1,
          max: 4
        }
      },
      onCreate: function(){ 
        $(this).addClass('init');
        $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        setTimeout(function() {
          $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        }, 500);
      }
    }).touchwipe({
      wipeLeft: function() {
        $('.foo4').trigger('next', 1);
      },
      wipeRight: function() {
        $('.foo4').trigger('prev', 1);
      },
			preventDefaultEvents: false
    });
  }
  
  if($(".foo5").exists()) {
    $('.foo5').carouFredSel({
      responsive: true,
      width: '100%',
      prev: '.prev5',
      next: '.next5',
      scroll: {
        items: 1,
        speed: 500,
        timeoutDuration:300000
			},
      items: {
        height: 'auto',
        visible: {
          min: 1,
          max: 4
        }
      },
      onCreate: function(){
        $(this).addClass('init');
        $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        setTimeout(function() {
          $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        }, 500);
      }
    }).touchwipe({
      wipeLeft: function() {
        $('.foo5').trigger('next', 1);
      },
      wipeRight: function() {
        $('.foo5').trigger('prev', 1);
      },
			preventDefaultEvents: false
    });
  }
  
  if($(".foo8").exists()) {
    $('.foo8').carouFredSel({
      responsive: true,
      width: '100%',
      prev: '.prev8',
      next: '.next8',
      scroll: {
        items: 1,
        speed: 500,
        timeoutDuration:300000
			},
      items: {
        width: 1170,
        height: 'auto',  
        visible: {
          min: 1,
          max: 1
        }
      },
      onCreate: function(){ 
        $(this).addClass('init');
        $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        setTimeout(function() {
          $(this).parent().add($(this)).css('height', $(this).children().first().height() + 'px');
        }, 500);
        
        var top = $(this).find('.img-block img').height();
        $(this).closest('.slider-foo-8').find('.prev, .next').css('top', top / 2);
      }
    }).touchwipe({
      wipeLeft: function() {
        $('.foo8').trigger('next', 1);
      },
      wipeRight: function() {
        $('.foo8').trigger('prev', 1);
      },
			preventDefaultEvents: false
    });
  }
}

function scrollMenu() {
  var $  = jQuery,
      link = $('.single-page-nav a');

  $(document).on('scroll', onScroll);
  
  link.on('click', function(e) {
    var target = $(this).attr('href'),
        $this = $(this);
      
    e.preventDefault();
    
    
    if ($(target).length) {
      $('html, body').animate({scrollTop: $(target).offset().top}, 600);
    }
  });
  
  function onScroll(){
    var scrollPos = $(document).scrollTop()+1;
  
    link.each(function () {
      var currLink   = $(this),
        refElement = $(currLink.attr('href'));
      
      if (
      refElement.position().top <= scrollPos &&
      refElement.position().top + refElement.height() > scrollPos) {
        link.removeClass('current');
        currLink.addClass('current');
      } else {
        currLink.removeClass('current');
      }
    });
  }
}

jQuery(document).ready(function(){
  'use strict';
  var $ = jQuery;

  if($('.slider-overlay').exists()) {
    titleParams();
    
    $( window ).load(function() {
      titleCanvas();
    });
  }
  
  
  carousels();
  scrollMenu();
});

//Window Resize
jQuery(window).on('resize', function() {
  var $ = jQuery;
  
  if($('.slider-overlay').exists()) {
    titleParams();
    titleCanvas();
  }
  
  carousels();
  scrollMenu();
});


/* ---------------- Blur ------------------*/

if(typeof($.fn.stellar) !== 'undefined') {
  if(!navigator.userAgent.match(/iPad|iPhone|Android/i) && ($('body').width()) >= 1023) {
    if($(".blur").exists()) {
      $(document).ready( function() {
        $('.blur .overlay').blurjs({
          source: '.blur',
          radius: 30,
          overlay: 'rgba(0, 0, 0, .2)'
        });
      });
    }
  }
}

/* ----------------------------- Contact Us form----------------------- */
$('#submit').click(function(){
  $.post('form.html', $('#contactform').serialize(),  function(data) {
    $('#success').html(data).animate({opacity: 1}, 500, function(){
  if ($(data).is('.send-true')) {
    $('#contactform').trigger( 'reset' );
  }
    });
  });
  return false;
});

/* ----------------------------- Newsletters form ----------------------- */
$('#newsletters-submit').click(function(){
  $.post('form-newsletter.html', $('#newsletters-form').serialize(),  function(data) {
    $('.success').html(data).animate({opacity: 1}, 500, function(){
  if ($(data).is('.send-true')) {
    $('#newsletters-form').trigger( 'reset' );
  }
    });
  });
  return false;
});


/* --------------------------- play-video ----------------------------- */

jQuery('.play-video').on('click', function (e) {
    var videoContainer = jQuery('.video-block');
    videoContainer.prepend('<iframe src="http://player.vimeo.com/video/22439234" width="500" height="281" class="stretch-both" frameborder="0" webkitallowfullscreen="webkitallowfullscreen" mozallowfullscreen="mozallowfullscreen" allowfullscreen="allowfullscreen"></iframe>');
    videoContainer.fadeIn(300);
    e.preventDefault();
});
// Close Video
jQuery('.close-video').on('click', function (e) {
    jQuery('.video-block').fadeOut(400, function () {
        jQuery("iframe", this).remove().fadeOut(300);
    });
});



/* --------------------------- Google 3D pie -----------------------*/
function drawChart() {
	var data = google.visualization.arrayToDataTable([
		['Task', 'Hours per Day'],
		['One',     25],
		['Two',      15],
		['Three',  16],
		['Four', 17],
		['Five',    12],
		['Six',    9]
	]);

	var options = {
		title: '',
		is3D: true,
		fontSize: 10,
		forceIFrame: true,
		legend: {position: 'right', textStyle: { color: '#777', fontSize: 12}},
		pieSliceText:'none',
		backgroundColor: 'none',
		slices: {0: {color: 'ff9f2d'}, 1: {color: 'fee400'}, 2: {color: '99af31'}, 3: {color: '2063ad'}, 4: {color: 'da615d'}, 5: {color: 'cd3333'}}
	};

	var chart = new google.visualization.PieChart(document.getElementById('piechart-3d'));
	chart.draw(data, options);
}
	
if($("#piechart-3d").exists()) {
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(drawChart);
}


/* ----------------------------- Add class if IE 11 or IE10 ------------------------------*/

var ua = navigator.userAgent,
  doc = document.documentElement;

if ((ua.match(/MSIE 10.0/i))) {
  doc.className = doc.className + " ie10";

} else if((ua.match(/rv:11.0/i))){
  doc.className = doc.className + " ie11";
}


/*----------------- Add Animate CSS  -----------------*/
//Animations
function animations() {

  //Calculating The Browser Scrollbar Width
  var parent, child, scrollWidth, bodyWidth;

  if (scrollWidth === undefined) {
    parent = jQuery('<div style="width: 50px; height: 50px; overflow: auto"><div/></div>').appendTo('body');
    child = parent.children();
    scrollWidth = child.innerWidth() - child.height(99).innerWidth();
    parent.remove();
  }

  $('[data-appear-animation]').each(function() {
  var $this = $(this);

  $this.addClass('appear-animation');

  if(!$('body').hasClass('no-csstransitions') && ($('body').width() + scrollWidth) > 767) {
    $this.appear(function() {
    var delay = ($this.attr('data-appear-animation-delay') ? $this.attr('data-appear-animation-delay') : 1);

    if(delay > 1) $this.css('animation-delay', delay + 'ms');
    $this.addClass($this.attr('data-appear-animation'));

    setTimeout(function() {
      $this.addClass('appear-animation-visible');
    }, delay);
    }, {accX: 0, accY: -150});
  } else {
    $this.addClass('appear-animation-visible');
  }
  });
  
  /* Animation Progress Bars */
  $('[data-appear-progress-animation]').each(function() {
  var $this = $(this);

  $this.appear(function() {
    var delay = ($this.attr('data-appear-animation-delay') ? $this.attr('data-appear-animation-delay') : 1);

    if(delay > 1) $this.css('animation-delay', delay + 'ms');
    
    $this.find('.progress-bar').addClass($this.attr('data-appear-animation'));

    setTimeout(function() {
    $this.find('.progress-bar').animate({
      width: $this.attr('data-appear-progress-animation')
    }, 500, 'easeInCirc', function() {
      $this.find('.progress-bar').animate({
      textIndent: 10
      }, 1500, 'easeOutBounce');
    });
    }, delay);
  }, {accX: 0, accY: -50});
  });
}



/*-------------------------------- Morris -------------------------*/
if($("#graph").exists()) {
  new Morris.Line({
    // ID of the element in which to draw the chart.
    element: 'graph',
    // Chart data records -- each entry in this array corresponds to a point on
    // the chart.
    data: [
      {"month": "2012-10", "sales": 4000, "rents": 5000},
      {"month": "2012-09", "sales": 4000, "rents": 5500},
      {"month": "2012-08", "sales": 3300, "rents": 5100},
      {"month": "2012-07", "sales": 3300, "rents": 5150},
      {"month": "2012-06", "sales": 3100, "rents": 4800},
      {"month": "2012-05", "sales": 2900, "rents": 4100},
      {"month": "2012-04", "sales": 2300, "rents": 4600},
      {"month": "2012-03", "sales": 2300, "rents": 3500},
      {"month": "2012-02", "sales": 2700, "rents": 1700},
      {"month": "2012-01", "sales": 2000, "rents": 1000}
    ],
    // The name of the data record attribute that contains x-values.
    xkey: 'month',
    // A list of names of data record attributes that contain y-values.
    ykeys: ['sales', 'rents'],
    // Labels for the ykeys -- will be displayed when you hover over the
    // chart.
    labels: ['sales', 'rents'],
    barRatio: 0.4,
    xLabelAngle: 35,
    hideHover: 'auto',
    smooth: false,
    resize: true,
    lineColors: ['#98b025','#d45050', '#000099']
  });
}

if($("#hero-bar").exists()) {
    Morris.Bar({
    element: 'hero-bar',
    data: [
      {month: 'Jan.', sales: 2000, rents:2400},
      {month: 'Feb.', sales: 3000, rents:3100},
      {month: 'Mar.', sales: 3600, rents:3000},
      {month: 'Apr.', sales: 4300, rents:4100},
      {month: 'May.', sales: 3300, rents:3500},
      {month: 'Jun.', sales: 3000, rents:3800},
      {month: 'Jul.', sales: 3400, rents:2900},
      {month: 'Aug.', sales: 2900, rents:3500},
      {month: 'Sep.', sales: 4000, rents:3500},
      {month: 'Oct.', sales: 3900, rents:3400}
    ],
    xkey: 'month',
    ykeys: ['sales', 'rents'],
    labels: ['sales', 'rents'],
    barRatio: 0.4,
    xLabelAngle: 35,
    hideHover: 'auto',
    resize: true,
    lineColors: ['#98b025','#d45050', '#000099']
  });
}

/* ---------------------------- jqplot Chart 1 --------------------------------- */
if($("#chart1").exists()) {
  var data = [
    ['One', 25],['Two', 15], ['Three', 16], 
    ['Four', 17],['Five', 12], ['Six', 15]
	];
	var plot1 = jQuery.jqplot ('chart1', [data], { 
		seriesDefaults: {
			shadow: false,
			renderer:$.jqplot.DonutRenderer,
		    rendererOptions: {
				startAngle: -90,
				diameter: 140,
				dataLabelPositionFactor: 0.6,
				innerDiameter: 28,
				showDataLabels: true
			}
		},
		grid:{
			background:'transparent',
			borderColor:'transparent',
			shadow:false,
			drawBorder:false,
			shadowColor:'transparent'
		},
		seriesColors: [
			"#3f4bb8",
			"#e13c4c",
			"#ff8137",
			"#ffbb42",
			"#20bdd0",
			"#2b70bf",
			"#f25463",
			"#f1a114",
			"#f5707d",
			"#ffd07d",
			"#4c7737"],
		legend: { 
			show:false, 
			location: 'e'
		}
	});
	$(window).resize(function() {
		plot1.replot( { resetAxes: true } );
	});
}

