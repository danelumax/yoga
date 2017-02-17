//扩展全局方法的插件... 
//jQuery 对外提供的扩展插件的一个借口..
$.extend({
	trimStr:function(str){
		str = str.replace(/^\s\s*/, "");
		var ws = /\s/;
		var i = str.length;
		while (ws.test(str.charAt(--i)));
		return str.slice(0, i + 1);
	}
	
})
