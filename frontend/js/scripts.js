$('.search-bar .icon').on('click', function() {
  $(this).parent().toggleClass('active');
});

var winHeight = $(".calendar").height();
var height = ( winHeight * 16.6666 ) / 100;
var lineHeight = height + "px";

$("#fullDiv li").css("line-height", lineHeight);
$("#fullDiv li").css("height", height);

$(".search-bar").change(function(){
  window.location.href = "/search";
});