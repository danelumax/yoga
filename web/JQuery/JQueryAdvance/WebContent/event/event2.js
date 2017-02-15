/**
 * 自定义事件
 *    事件必须满足三个条件：
 *       1、事件必须有名称
 *       2、事件必须绑定在某一个对象上
 *       3、事件必须有触发条件
 */
/**
 * 给div添加一个事件，该事件的名称为"itheima12很牛",当点击div的时候，触发click事件的同时触发"itheima12很牛"事件
 */
$().ready(function(){
	$("div").unbind("click");
	$("div").bind("click",function(){
		/**
		 * 在点击div的时候，触发customerEvent事件
		 */
		//$(this).trigger("customerEvent",5);
		//$(this).trigger("itheima12很牛",[5,6]);
		$(this).trigger("customerEvent",{
			aa:'aa',
			bb:'bb'
		});
	});
	
	$("div").unbind("customerEvent");
	$("div").bind("customerEvent",function(event,json){
		alert(json.aa);
		alert(json.bb);
	});
});
