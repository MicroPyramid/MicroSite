/*$(document).ready(function(e){
	alert('');
})*/
$('#trigger').click(function(e){
	e.stopPropagation();
	$('#mp-pusher').addClass('mp-pushed').css('transform','translateX(300px)');
	$('#mp-menu .mp-level:first-child').addClass('mp-level-open');
});
$('.mp-level ul li a').click(function(e){
	e.stopPropagation();
	$('#mp-menu').addClass('mp-overlap');
	$(this).parent('.mp-level-open').addClass('mp-level-overlay');
	$('#mp-pusher').css('transform','translateX(340px)');
	$(this).next('.mp-level').addClass('mp-level-open');
})
/*$('.mp-level').click(function(e){
	e.stopPropagation();
})*/
$('body').click(function(e){
	$('#mp-pusher').removeClass('mp-pushed').css('transform','translateX(0px)');
	$('.mp-level').removeClass('mp-level-open');
})
$('.mp-back').click(function(e){
	$(this).parent('.mp-level').removeClass('mp-level-open mp-level-overlay');
	$('#mp-pusher').css('transform','translateX(300px)');
})