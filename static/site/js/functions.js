jQuery(document).ready(function($) {
    "use strict";
    jQuery('ul.sf-menu').superfish({
        animation: {
            height: 'show'
        },
        animationOut: {
            height: 'hide'
        },
        speed: 'fast',
        speedOut: 'fast',
        delay: 800,
        pathClass: 'current'
    });
    jQuery.fn.toggle = function(fn, fn2) {
        if (!jQuery.isFunction(fn) || !jQuery.isFunction(fn2)) {
            return oldToggle.apply(this, arguments);
        }
        var args = arguments,
            guid = fn.guid || jQuery.guid++,
            i = 0,
            toggler = function(event) {
                var lastToggle = (jQuery._data(this, "lastToggle" + fn.guid) || 0) % i;
                jQuery._data(this, "lastToggle" + fn.guid, lastToggle + 1);
                event.preventDefault();
                return args[lastToggle].apply(this, arguments) || false;
            };
        toggler.guid = guid;
        while (i < args.length) {
            args[i++].guid = guid;
        }
        return this.click(toggler);
    };
    var navlist = jQuery('.site-menu > nav ul').clone();
    var submenu = '<span class="submenu"></span>';
    navlist.removeClass().addClass('mobile-menu bottom-0 list-unstyled');
    navlist.find('ul').removeAttr('style');
    navlist.find('.menu-normal .sf-with-ul').after(submenu);
    navlist.find('.submenu').toggle(function() {
        jQuery(this).parent().addClass('over').find('>ul').slideDown(200);
    }, function() {
        jQuery(this).parent().removeClass('over').find('>ul').slideUp(200);
    });
    jQuery('#mobile-menu .menu-content').after(navlist[0]);
    jQuery('#mobile-menu').mmenu({
        position: "right",
        zposition: "front"
    });

    jQuery('*[data-toggle="tooltip"]').tooltip();  
    jQuery('.fixedheader').affix({
        offset: {
            top: 40
        }
    });
    jQuery('.fullfixed').affix({
        offset: {
            top: 90
        }
    });
});
