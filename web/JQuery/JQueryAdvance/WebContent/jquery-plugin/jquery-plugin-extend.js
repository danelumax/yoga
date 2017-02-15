/*
 * 扩展jQuery元素来提供新的方法
 */

(function(jQuery){
	jQuery.fn.myextend = function(json){
		for(var i in json){
			jQuery.fn[i] = json[i];
		}
	}
	
	jQuery.myextend = function(json){
		for(var i in json){
			jQuery[i] = json[i];
		}
	}
})(jQuery);

$().ready(function(){
	$("body").myextend({
		aa:function(){
			alert("aa");
		}
	});
	$("body").aa();
});
