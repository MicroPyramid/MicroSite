$('body').scrollTop(0);
/* initial banner height */
function change_banner_height(){
	var window_height=$(window).height();
	var menu_height;
	if($(window).width()>767){
		menu_height=$('#base_menu').height();
	}
	else{
		menu_height=$('#mob_menu').height();
	}
	banner_height= window_height - menu_height;
	return banner_height
}
$('.intro_banner').css('height',change_banner_height());
$(window).resize(function(e) {
	change_banner_height();
});
$('.wrap_child').css('height',change_banner_height());
/* initial banner height */

/* inital banner text slide */
function title_pading(){
	$('.intro_banner .title span').last().css('padding-left',$('.green.active').width()+10)
}
function change_title(_title_index){
	$('.intro_banner .title .green').eq(_title_index).delay(5000).addClass('active').siblings().removeClass('active');
	title_pading();
}
function change_text(_text_index){
	$('.intro_banner .content .each_content').eq(_text_index).delay(5000).addClass('active').siblings().removeClass('active');
}
/* initial banner text slide */

/* tumbnails div */
$('.tumbnail_each').click(function(e){
	tumb_index($(this).index());
})
function tumb_index(_thumb_index){
	$('.tumbnail_each').removeClass('active');
	$('.tumbnails_div').children('.tumbnail_each').eq(_thumb_index).addClass('active');
	change_title(_thumb_index);
	change_text(_thumb_index);
	slide_right(_thumb_index);
}
/* tumbnails_div */

/* image slider */
function set_slider_wid(){
	var img_wid = $('.right_slider').width();
	var slides_count = $('.slider_wrap .img').length;
	//console.log('no.of slides: '+ slides_count);
	$('.slider_wrap .img').css('width',img_wid);
	var slider_wrap_wid = img_wid*slides_count+(slides_count*10);
	$('.slider_wrap').css('width',slider_wrap_wid)
}
function slide_right(_thumb_index){
	var animate_wid = $('.slider_wrap .img').width()*_thumb_index+(_thumb_index*10);
	if($('.tumbnails_div .tumbnail_each').length==_thumb_index){
		$('slider_wrap').animate({left:0},200);
	}
	else{
		$('.slider_wrap').animate({left:'-'+animate_wid+'px'},200)
	}
}
/* image slider */

/* page load function calls */
title_pading();
set_slider_wid();

setInterval(function(e){
	if($('.tumbnail_each.active').index()==$('.slider_wrap .img').length-1){
		$('.tumbnail_each').first().click();
	}
	else{
		$('.tumbnail_each.active').next().click();
	}
},3000)
/* page load function calls */
/* horizontal scroll_div width */
if($(window).width()>767){
	$('.horizontal_child').css('width',$('body').width());
	$('.horizontal_wrap_scroll').css('width',$('.horizontal_child').width()*$('.horizontal_child').length)
}
/* horizontal scroll div width */


/* scroll */
$(window).scroll(function(e){
	scroll_action();
})
function scroll_action(){
	if($(window).width()>767){
		$('body').unbind('mousewheel');
		var content_height= $('.wrap_child').height();
		if($(window).scrollTop() > content_height && $(window).scrollTop() < (content_height+150)){
			mouse_stop();
		}
		else{
			mouse_bind();
		}
	}
}
function mouse_stop(){
	$('body').bind('mousewheel',function(e,delta){
		e.preventDefault();
		e.stopPropagation();
		//console.log('scroll top value : '+$('body').scrollTop())
		$('body').stop(true).animate({scrollTop:($('.wrap_child').height()+10)},1000);
		if($('.horizontal_wrap').scrollLeft()==0){
			if(e.originalEvent.wheelDelta>0){
				$('body').stop(true).animate({scrollTop:'-='+40},10);
					//mouse_bind();
			}
			else{
				$('.horizontal_wrap').stop(true).animate({scrollLeft:'+='+40},10);
			}
		}
		/* detect max horizontal scroll */
		else if($('.horizontal_wrap').scrollLeft() == $('.horizontal_wrap_scroll').width()-$('.horizontal_child').width()){
			if(e.originalEvent.wheelDelta>0){
				$('.horizontal_wrap').stop(true).animate({scrollLeft:'-='+40},10)
			}
			else{
				$('body').stop(true).animate({scrollTop:'+='+$('.wrap_child').height()},600)
			}
		}
		/* detect max horizontal scroll */
		else{
			if(e.originalEvent.wheelDelta>0){
				$('.horizontal_wrap').stop(true).animate({scrollLeft:'-='+40},10);
			}
			else{
				$('.horizontal_wrap').stop(true).animate({scrollLeft:'+='+40},10);
			}
		}
	});
}
function mouse_bind(){
	$('body').bind('mousewheel',function(e){
		e.preventDefault();
		e.stopPropagation();
		// get_max_reset();
		if(e.originalEvent.wheelDelta>0){
			$('body').stop(true).animate({scrollTop:'-='+40},10);
		}
		else if(e.originalEvent.wheelDelta<0){
			$('body').stop(true).animate({scrollTop:'+='+40},10);
		}
	})
}
/* scroll */
if($(window).width()<767){
	$('.horizontal_wrap, .strengths').css('height','auto');
}
$('body').animate({scrollTop:'0'},100);
/* key press disable */
$('body').keydown(function(e){
	//alert(e.keyCode)
	if(e.keyCode==40 || e.keyCode==38){
		e.preventDefault();
		e.stopPropagation();
		//scroll_action();
	}
})
/* key press disable */
if($(window).width()>767){
var ts, tx;
$(document).bind('touchstart', function (e){
		e.preventDefault();
		e.stopPropagation();
   ts = e.originalEvent.touches[0].clientY;
   tx = e.originalEvent.touches[0].clientX;
});

$(document).bind('touchend', function (e){
   var te = e.originalEvent.changedTouches[0].clientY;
   var txe = e.originalEvent.changedTouches[0].clientX;
   var height_scroll=$('.wrap_child').height();
   var width_scroll=$('.wrap_child').width();
   if(ts > te+5){
   	if($('body').scrollTop()==height_scroll){
   		if($('.horizontal_wrap').scrollLeft()==$('.horizontal_wrap_scroll').width()-$('.horizontal_child').width()){
   			scroll_down_touch(height_scroll);
   		}
   		else{
   			scroll_left_touch(height_scroll,width_scroll);
   		}
   	}
   	else{
   		scroll_down_touch(height_scroll);
   	}
   }
   else if(ts < te-5){
   	if($('body').scrollTop()==height_scroll){
   		if($('.horizontal_wrap').scrollLeft()==0){
   			scroll_top_touch(height_scroll);
   		}
   		else{
   			scroll_right_touch(height_scroll,width_scroll);
   		}
   	}
   	else{
   		scroll_top_touch(height_scroll);
   	}
   }
   else if(tx > txe+5){
   	scroll_left_touch(height_scroll,width_scroll);
   }
   else if(tx< txe-5){
   	scroll_right_touch(height_scroll,width_scroll);
   }
});
function scroll_left_touch(height_scroll,width_scroll){
	$('body').animate({scrollTop:height_scroll}, 100);
	$('.horizontal_wrap').animate({scrollLeft:'+='+width_scroll},100);
}
function scroll_right_touch(height_scroll,width_scroll){
	$('body').animate({scrollTop:height_scroll}, 100);
	$('.horizontal_wrap').animate({scrollLeft:'-='+width_scroll},100);
}
function scroll_top_touch(height_scroll){
	$('body').animate({scrollTop:'-='+height_scroll}, 100);
}
function scroll_down_touch(height_scroll){
	$('body').animate({scrollTop:'+='+height_scroll}, 100);

}
}