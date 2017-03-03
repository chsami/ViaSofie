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


/**********************/
/*	Client carousel   */
/**********************/
$(window).load(function() {
    $('.carousel-client').bxSlider({
        auto: true,
        slideWidth: 234,
        minSlides: 2,
        maxSlides: 5,
        controls: false
    });
});


/**********************/
/*   	Bollen        */
/**********************/

$(function() {
	$(window).resize(function() {
		resizeTrafficLightText();
	});

	resizeTrafficLightText();
});

function resizeTrafficLightText() {
	$(".traffic-light-right").each(function(i, circle) {
		var text = $(circle).find("span");
		var circleW, circleH, textW, textH, textSize, leftPos, topPos;

		circleW = $(circle).width();
		circleH = $(circle).height();

		textSize = circleW * 0.7;
		$(text).css('font-size', textSize);
		while (($(text).width() * 1.2) > circleW ) {
			$(text).css('font-size', --textSize);
		}    

		leftPos = (circleW - $(text).width()) / 2; 
		topPos = (circleW - $(text).height()) / 2;

		$(text).css('left', leftPos);
		$(text).css('top', topPos);
	});


    $(".traffic-light-left").each(function(i, circle) {
		var text = $(circle).find("span");
		var circleW, circleH, textW, textH, textSize, leftPos, topPos;

		circleW = $(circle).width();
		circleH = $(circle).height();

		textSize = circleW * 0.7;
		$(text).css('font-size', textSize);
		while (($(text).width() * 1.2) > circleW ) {
			$(text).css('font-size', --textSize);
		}    

		leftPos = (circleW - $(text).width()) / 2; 
		topPos = (circleW - $(text).height()) / 2;

		$(text).css('left', leftPos);
		$(text).css('top', topPos);
	});
}