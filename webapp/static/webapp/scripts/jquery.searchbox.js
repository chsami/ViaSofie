(function($) {
  var productSearch,
      productInput, siteSearch, siteInput,
      productButton, siteButton, megaSearch,
      searchField;
  
  function onDocumentReady() {
    megaSearch = $(document.getElementById('mega-search'));
    productSearch = $(document.getElementById('mega-productsearch'));
    productInput = $(document.getElementById('mega-p-s'));
    productButton = $(document.getElementById('product-submit'));
    siteSearch = $(document.getElementById('mega-sitesearch'));
    siteInput = $(document.getElementById('mega-s'));
    siteButton = $(document.getElementById('full-site-submit'));
    searchField = megaSearch.find('.search-form-input');
    
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
			focusedParent = focused.closest('.search-form'),
			sibling = focusedParent.siblings('.search-form');


		if (focusedParent.hasClass('inactive')) {

			focusedParent.removeClass('inactive').addClass('active')
			.stop(true, false).velocity({
				translateX: 0,
				translateZ: 0
			}, 300)
			.stop(true, false).velocity({
				opacity:1,
				translateY: 0
			}, {delay:200}, 300)
			.find('.button').stop(true, false).velocity('fadeIn', {delay: 600}, {duration:300}, "ease");

			sibling.removeClass('active').addClass('inactive')	
			.stop(true, false).velocity({
				translateX: '-120px',
				translateZ: '-67px'
			}, 300)
			.stop(true, false).velocity({
				opacity: 0.39,
				translateY: '0px'
			}, {delay:200}, 300)
			.find('.button').stop(true, false).velocity('fadeOut', {duration:10});
		}
	}
  
  $(onDocumentReady);
  
})(jQuery);