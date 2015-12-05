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
	console.log(index_val);
	index_val++;
	$('.dots_wrap ul li:nth-child('+index_val+')').addClass('active').siblings().removeClass('active');
	$('.daimond_tabs ul li:nth-child('+index_val+')').addClass('active').siblings().removeClass('active');
	//$('.tab_text_wrap').fadeOut('slow');
	$('.tab_text_wrap:nth-child('+index_val+')').siblings().hide();
	$('.tab_text_wrap:nth-child('+index_val+')').fadeIn('slow');
}
setInterval(function(){
	var current_active=$('.daimond_tabs ul li.active').index()+1
	if(current_active==$('.daimond_tabs ul li').length){
		current_active=0
	}
	active(current_active);
 }, 3000);
/* slider */
/* scroll */
$(window).scroll(function(e){
	console.log('scrolled');
	console.log($(window).width())
	console.log($(window).scrollTop())
	if($(window).width()>991 && $(window).scrollTop()>550){
		$('#menu_wrapper').addClass('fixed_menu')
		console.log('yes');
	}
	else if($(window).width()<992 && $(window).scrollTop()>500){
		$('#menu_wrapper').addClass('fixed_menu')
	}
	else{
		$('#menu_wrapper').removeClass('fixed_menu');
	}
})
/* scroll */
