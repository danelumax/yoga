$().ready(function(){
	
	/**
	 * 给指定的区域中的指定的元素添加指定的事件
	 *   能给未来的元素添加指定的事件
	 * @param {Object} "input[type='button']"
	 */
	// 能为后续添加的元素指定事件
	// 但是无法避免事件叠加
	$("body").delegate("div","click",function(){
		alert("aaaa");
	});
	
	$("input[type='button']").unbind("click");
	$("input[type='button']").bind("click",function(){
		$("body").append($("<div/>").text("aaaaa"));
	});
	for(var i=0;i<3;i++){
		/**
		 * 用click的方法声明事件，事件是可以叠加的
		 * 该方法不能给未来的元素添加事件
		 * 直接用click添加回调事件是最弱的
		 */
//		$("div").click(function(){
//			alert("aaa");
//		});
		
		/**
		 * 可以避免事件叠加
		 * 也不能给未来的元素添加事件
		 */
//		$("div").unbind("click");//使该属性从该对象上移除
//		$("div").bind("click",function(){
//			alert("aaa");
//		});
	}
});
