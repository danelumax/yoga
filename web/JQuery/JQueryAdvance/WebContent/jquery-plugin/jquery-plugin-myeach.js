(function(jQuery){
	//选择器
	jQuery.fn.myeach = function(callback){
		//this 代表调用each的选择器返回对象， 是一个数组
		var array = $(this);
		for(var i=0;i<array.length;i++){
			//不能用this，this是多个，应该是一个元素一个元素调用
			callback.call($(array[i]),$(array[i]));
		}
	}
	/**
	 * @param {Object} obj  可以来自于利用jquery的选择器创建的jquery对象，也可以来自于一个数组(来源于后台)
	 * @param {Object} callback
	 */
	//全局
	jQuery.myeach = function(obj,callback){
		//指定jQuery对象
		var array = obj;
		for(var i=0;i<array.length;i++){
			//this代表当前正在遍历的对象
			callback.call($(array[i]),$(array[i]));
		}
	}
})(jQuery);

$().ready(function(){
	$("div").myeach(function(){
		//this代表当前正在遍历的单个div对象
		alert($(this).text());
	});
	
	$.myeach($("div"),function(e){
		alert($(e).text());
	});
});
