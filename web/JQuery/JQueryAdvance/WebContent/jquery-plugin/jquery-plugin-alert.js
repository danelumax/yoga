(function($){
	$.alert = function(msg){
		window.alert("plugin: " + msg);
	}
	
	// fn 是选择器返回的对象
	$.fn.alert = function(msg){
		window.alert("select: " + msg);
	}
})($);

$().ready(function(){
	$.alert("aaaaa");
	//$("body")返回选择器jQuery对象
	$("body").alert("bbbb");
});
