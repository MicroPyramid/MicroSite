$( document ).ready(function() {
    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='mobile-nav-top']", function() {
      $("[data-toggle='wy-nav-shift']").toggleClass("shift");
    });
  
});
