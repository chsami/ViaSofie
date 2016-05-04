// navigation slide-in
$(window).load(function() {
    $('.nav_slide_button').click(function() {
        $('.pull').slideToggle();
    });
});

$(function() {
    $("#slider").responsiveSlides({
        auto: true,
        speed: 500,
        namespace: "callbacks",
        pager: true,
    });
});

addEventListener("load", function() { setTimeout(hideURLbar, 0); }, false);

function hideURLbar() { window.scrollTo(0, 1); }
