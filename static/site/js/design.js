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


