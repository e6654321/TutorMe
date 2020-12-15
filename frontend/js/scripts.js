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

var message = $("#messages").text();
const reDirect = ()=>{
    if(message == "You are not a mentor. You will be redirected momentarily."){      
      setTimeout(()=>{
        window.location.href="/search";
      }, 5000);
  }
};


reDirect();