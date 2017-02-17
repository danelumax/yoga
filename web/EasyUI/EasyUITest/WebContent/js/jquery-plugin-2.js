//扩展局部方法的插件


$.fn.extend({
	datagrid:function(object){
		var coloums=object.coloums;
		var tr="<tr>";
		for(var i=0;i<coloums.length;i++){
			tr+="<td>"+coloums[i].title+"</td>";
		}
		tr+="</tr>";
		$(this).append(tr);	
		$.ajax({
			url:object.url,
			type:object.method,
			success:function(data){
				var rows=data.rows;
				for(var i=0;i<rows.length;i++){
					var tr1="<tr>";
					tr1+="<td>"+rows[i].number+"</td>";
					tr1+="<td>"+rows[i].ceci+"</td>";
					tr1+="<td>"+rows[i].startstate+"</td>";
					tr1+="<td>"+rows[i].starttime+"</td>";
					tr1+="<td>"+rows[i].yz+"</td>";
					tr1+="<td>"+rows[i].bz+"</td>";
					tr1+="</tr>";
					$("#datagrid").append(tr1);
				}
			}
		})
	}
})