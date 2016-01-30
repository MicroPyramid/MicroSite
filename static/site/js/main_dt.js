$('#menu_wrapper').click(function(e){
	e.stopPropagation;
})
$('body').click(function(e){
	$('body').hover();
})
/* slider */

$('.slider_footer .daimond_tabs ul li, .dots_wrap ul li ').click(function(e){
	e.stopPropagation();
	e.preventDefault();
	var index_val=$(this).index();
	active(index_val)
})
function active(index_val){
   index_val++;
   $('.dots_wrap ul li:nth-child('+index_val+')').addClass('active').siblings().removeClass('active');
   $('.daimond_tabs ul li:nth-child('+index_val+')').addClass('active').siblings().removeClass('active');
   //$('.tab_text_wrap').fadeOut('slow');
   $('.tab_text_wrap:nth-child('+index_val+')').siblings().hide();
   $('.tab_text_wrap:nth-child('+index_val+')').fadeIn('slow').css({"display":"table-cell","vertical-align":"middle"});
}
setInterval(function(){
	var current_active=$('.daimond_tabs ul li.active').index()+1
	if(current_active==$('.daimond_tabs ul li').length){
		current_active=0
	}
	active(current_active);
 }, 5000);
/* slider */
/* scroll */
$(window).scroll(function(e){
	if($(window).width()>991 && $(window).scrollTop()>500){
		$('#menu_wrapper').addClass('fixed_menu')
	}
	else{
		$('#menu_wrapper').removeClass('fixed_menu');
	}
})
/* scroll */
 /* contact pop up */
$('.conatact_us_icon, .contact_mob').click(function(e){
	e.preventDefault();
	e.stopPropagation();
	$('.overlay_contact').show();
	$('.contact_div_wrap').fadeIn('fast');
});
$('.contact_div_wrap').click(function(e){
	e.stopPropagation();
});
$('.overlay_contact, .close_contact').click(function(e) {
	e.preventDefault();
	$('.overlay_contact').hide();
	$('.contact_div_wrap').hide();
});

$('.subscribe_icon, .subscribe_mob, .subscribe').click(function(e){
	e.preventDefault();
	e.stopPropagation();
	$('.overlay_subscribe').show();
	$('.subscribe_div_wrap').fadeIn('fast');
});
$('.subscribe_div_wrap').click(function(e){
	e.stopPropagation();
});
$('.overlay_subscribe, .close_subscribe').click(function(e) {
	e.preventDefault();
	$('.overlay_subscribe').hide();
	$('.subscribe_div_wrap').hide();
});

$("form#subscribeform").submit(function(e) {
e.preventDefault();
$.ajax({
  type: "POST",
  dataType: 'json',
  url: "/subscribe/",
  data: $('#subscribeform').serialize(), // from form
  success: function(data) {
    if (data.error) {
      $('p.failure').remove();
      for (var key in data.errinfo) {
        $('#subscribe-' + key).after('<p class="failure" style="color:red;">' + data.errinfo[key] + '</p>');
      }
    } else {
      alert(data.response);
      window.location = ".";
    }
  }
});
return false;
});

$("form#contactform").submit(function(e) {
e.preventDefault();
$.ajax({
  type: "POST",
  dataType: 'json',
  url: "/contact-us/",
  data: $('#contactform').serialize(), // from form
  success: function(data) {
    if (data.error) {
      $('p.failure').remove();
      for (var key in data.errinfo) {
        $('#' + key).after('<p class="failure" style="color:red;">' + data.errinfo[key] + '</p>');
      }
    } else {
      alert("Your message has been successfully sent. We will get back to you very soon!");
      window.location = "/";
    }
  }
});
return false;
});

$('body').keyup(function(e){
    if(e.which == 27){
       $('.overlay_contact').click();
    }
});
 /* contact pop up */
 /* web development technologies tabs */
function change_tab(_index_row,_index_element){
	$('.tech_daimond_wrap .tect_each_wrap').removeClass('active');
	$('.tech_daimond_wrap .row').eq(_index_row).children('a').eq(_index_element).children('.tect_each_wrap').addClass('active');
	var current_active=(_index_row*3)+_index_element;
	$('.tech_content .tab_content_each').removeClass('active');
	$('.tech_content .tab_content_each').eq(current_active).addClass('active');
}
$('.tech_daimond_wrap a').click(function(e){
	if($(window).width()>767){
		e.preventDefault();
		var _index_row=$(this).parent('.row').index()
		var _index_element=$(this).index()
		change_tab(_index_row,_index_element);
	}
});

 /* web development technologies tabs */
$(document).ready(function(n){
	//$('.map').addClass('logo');
})
