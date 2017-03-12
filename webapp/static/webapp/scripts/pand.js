// ZOOM ZOOM !!!

$('.product-preview').click(function(){
  $('.zoom-btn').toggleClass('active');
  $(this).toggleClass('activeZoom');
  $('.zoom-view').toggle();
});

$(document).on('mousemove', '.activeZoom', function(event){        
  var relX = event.pageX - $(this).offset().left;
  var relY = event.pageY - $(this).offset().top;
  var relBoxCoords = "(" + relX + "," + relY + ")";
  console.log(relBoxCoords);   
  
  zoomW =  $('.zoom-view').width();
  zoomH =  $('.zoom-view').height();
  $('.zoom-view').css('top',relY-(zoomH/2));
  $('.zoom-view').css('left',relX-zoomW/2);

  width = $(this).width();
  height = $(this).height();
  pX = (relX/width);
  pY = (relY/height);
  zimgW =  $('#zoom-image').width();
  zimgH =  $('#zoom-image').height();
  zX = (zimgW * pX)-(zoomW/1.375);
  zY = (zimgH * pY)-(zoomH/2);
  $('#zoom-image').css('top', '-' + zY + 'px' );
  $('#zoom-image').css('left', '-' + zX + 'px' );
});




$(document).ready(function() {
  var url = window.location;
  var title = document.title;
  var mnsocial = document.getElementsByClassName('mn-social-bottom');
  mnsocial[0].href = 'https://www.facebook.com/sharer/sharer.php?u=' + url;
  mnsocial[1].href = 'https://twitter.com/home?status=' + url + ' ' + title;
  mnsocial[2].href = 'https://www.linkedin.com/shareArticle?mini=true&url=' + url;
  mnsocial[3].href = 'https://plus.google.com/share?url=' + url;
  mnsocial[4].href = 'https://pinterest.com/pin/create/link/?url=' + url;
  mnsocial[6].href = 'http://www.tumblr.com/share/link?url=' + url;
  mnsocial[7].href = 'https://getpocket.com/save?url=' + url;
  mnsocial[8].href = 'http://www.stumbleupon.com/submit?url=' + url;
  mnsocial[9].href = 'http://www.reddit.com/submit?url=' + url;
  mnsocial[10].href = 'mailto:?&subject=' + url + '&body=' + title + ', ' + url;
  mnsocial[11].href = 'https://delicious.com/share?url=' + url;
});