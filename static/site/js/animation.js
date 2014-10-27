function el_animate() {
    var delay, speed, prog;
    jQuery('.animated').each(function() {
        var el = jQuery(this);
        //console.log( elements[i] , i );
        if (el.visible(true)) {
			// Checking if to animate for Dial Skills
			
			if(el.hasClass('countPercentage')){
				//var element = jQuery('.countPercentage');
				//console.log(el.children('span'));
				var percentageto = el.data('percentageto');
				var animdelay = el.data('animdelay');
				
				animate_percentage(el.children('span'), percentageto, animdelay);
			
			}
			
            delay = el.data('animdelay');
            if (!delay) {
                delay = 0;
            }
			
            el.css('-webkit-animation-delay', delay);
            el.css('-moz-animation-delay', delay);
            el.css('-o-animation-delay', delay);
            el.css('animation-delay', delay);

            speed = el.data('animspeed');

            if (!speed) {
                speed = 0.5;
            }

            el.css('-webkit-animation-duration', speed);
            el.css('-moz-animation-duration', speed);
            el.css('-o-animation-duration', speed);
            el.css('animation-duration', speed);

         /*el.delay(1000)
.queue( function(){

					if (el.data('animtype')) {
						el.addClass(el.data('animtype'));
					}
					el.addClass('animated_visible');
				});*/
			
			if (el.data('animtype')) {
				el.addClass(el.data('animtype'));
			}
			el.addClass('animated_visible');
					
            // que.push(this);
        }
        else if (el.data('animrepeat') == '1') {
            el.removeClass(el.data('animtype'));
            el.removeClass('animated_visible');
        }
		
    });
}

//jQuery(window).ready(el_animate);
//jQuery(window).load(el_animate);


jQuery(window).scroll(function(event) {
    el_animate();
});

	// Animating Percentage
/*	var element = jQuery('.countPercentage');
	var el = element.children('span');
	var percentageto = jQuery('.countPercentage').data('percentageto');
	
	animate_percentage(el, percentageto, 15);*/
	
	function animate_percentage( display , percent_to, speed){
		
	
		var currentValue = parseInt(display.text());
		var nextValue    = percent_to;
		
		var diff         = nextValue - currentValue;
		var step         = ( 0 < diff ? 1 : -1 ); 
	
		for (var i = 0; i < Math.abs(diff); ++i) {
			setTimeout(function() {
				currentValue += step;
				display.text(currentValue);
			}, speed * i);
		}
	}	
	
	
	/*
 * Viewport - jQuery selectors for finding elements in viewport
 *
 * Copyright (c) 2008-2009 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *  http://www.appelsiini.net/projects/viewport
 *
 */
(function($) {


    /**
     * Copyright 2012, Digital Fusion
     * Licensed under the MIT license.
     * http://teamdf.com/jquery-plugins/license/
     *
     * @author Sam Sehnert
     * @desc A small plugin that checks whether elements are within
     *     the user visible viewport of a web browser.
     *     only accounts for vertical position, not horizontal.
     */

    $.fn.visible = function(partial) {

        var $t = $(this),
                $w = $(window),
                viewTop = $w.scrollTop(),
                viewBottom = viewTop + $w.height(),
                _top = $t.offset().top,
                _bottom = _top + $t.height(),
                compareTop = partial === true ? _bottom : _top,
                compareBottom = partial === true ? _top : _bottom;

        return ((compareBottom <= viewBottom) && (compareTop >= viewTop));

    };
})(jQuery);