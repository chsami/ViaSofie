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