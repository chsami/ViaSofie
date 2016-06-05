(function($) {
    var productSearch,
        productInput, siteSearch, siteInput,
        productButton, siteButton, megaSearch,
        searchField;

    function onDocumentReady() {
        megaSearch = $(document.getElementById('geavanceerd-search'));
        productSearch = $(document.getElementById('geavanceerd-productsearch'));
        productInput = $(document.getElementById('geavanceerd-p-s'));
        productButton = $(document.getElementById('product-submit'));
        siteSearch = $(document.getElementById('geavanceerd-sitesearch'));
        siteInput = $(document.getElementById('geavanceerd-s'));
        siteButton = $(document.getElementById('full-site-submit'));
        searchField = megaSearch.find('.geavanceerd-search-form-input');

        if (megaSearch.length > 0) {
            searchFormInit();
            searchField.on('click', onInactiveFocus);
        }
    }

    function searchFormInit() {
        siteSearch.stop(true, false).velocity({
            opacity: 0.39,
            translateX: '-120px',
            translateY: '0px',
            translateZ: '-62px'
        }, 0);

        productSearch.stop(true, false).velocity({
            opacity: 1,
            translateX: 0,
            translateY: 0,
            translateZ: 0
        }, 0);

        productButton.on('click', function() {
            return false;
        });
        siteButton.on('click', function() {
            return false;
        });
    }

    function onInactiveFocus(e) {
        var focused = $(e.currentTarget),
            focusedParent = focused.closest('.geavanceerd-search-form'),
            sibling = focusedParent.siblings('.geavanceerd-search-form');


        if (focusedParent.hasClass('inactive')) {

            focusedParent.removeClass('inactive').addClass('active')
                .stop(true, false).velocity({
                    translateX: 0,
                    translateZ: 0
                }, 300)
                .stop(true, false).velocity({
                    opacity: 1,
                    translateY: 0
                }, { delay: 200 }, 300)
                .find('.button').stop(true, false).velocity('fadeIn', { delay: 600 }, { duration: 300 }, "ease");

            sibling.removeClass('active').addClass('inactive')
                .stop(true, false).velocity({
                    translateX: '-120px',
                    translateZ: '-67px'
                }, 300)
                .stop(true, false).velocity({
                    opacity: 0.39,
                    translateY: '0px'
                }, { delay: 200 }, 300)
                .find('.button').stop(true, false).velocity('fadeOut', { duration: 10 });
        }
    }

    $(onDocumentReady);

})(jQuery);

$(function() {
    $("#aantal-slaapkamers-slider").slider({
        range: true,
        min: 1,
        max: 20,
        values: [2, 3],
        slide: function(event, ui) {
            $("#aantal-slaapkamers").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#aantal-slaapkamers").val("$" + $("#aantal-slaapkamers-slider").slider("values", 0) +
        " - $" + $("#aantal-slaapkamers-slider").slider("values", 1));
});

$(function() {
    $("#aantal-badkamers-slider").slider({
        range: true,
        min: 1,
        max: 10,
        values: [1, 2],
        slide: function(event, ui) {
            $("#aantal-badkamers").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#aantal-badkamers").val("$" + $("#aantal-badkamers-slider").slider("values", 0) +
        " - $" + $("#aantal-badkamers-slider").slider("values", 1));
});

$(function() {
    $("#aantal-verdiepen-slider").slider({
        range: true,
        min: 1,
        max: 5,
        values: [2, 3],
        slide: function(event, ui) {
            $("#aantal-verdiepen").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#aantal-verdiepen").val("$" + $("#aantal-verdiepen-slider").slider("values", 0) +
        " - $" + $("#aantal-verdiepen-slider").slider("values", 1));
});

$(function() {
    $("#prijs-range-slider").slider({
        range: true,
        min: 1,
        max: 1000000,
        values: [300000, 400000],
        slide: function(event, ui) {
            $("#prijs-range").val("$" + ui.values[0] + " - $" + ui.values[1]);
        }
    });
    $("#prijs-range").val("$" + $("#prijs-range-slider").slider("values", 0) +
        " - $" + $("#prijs-range-slider").slider("values", 1));
});