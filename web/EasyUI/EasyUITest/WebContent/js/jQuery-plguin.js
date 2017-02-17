$.fn.extend({
	datagrid:function(object){
		var columns=object.columns;
		var tr="<tr>";
		for(var i=0;i<columns.length;i++){
			tr+="<td>"+columns[i].title+"</td>";
		}
		tr+="</tr>";
		//this 一般是指代dom 对象，我们可以把它包装成jQUERY 对象..
		$(this).append(tr);
		//object.url
		$.ajax({
			url:object.url,
			type:object.method,
			success:function(data){
				//alert(data);
				var rows=data.rows;
				
				for(var i=0;i<rows.length;i++){
					var tr1="<tr>";
					tr1+="<td>"+rows[i].ceci+"</td>";
					tr1+="<td>"+rows[i].startstate+"</td>";
					tr1+="<td>"+rows[i].starttime+"</td>";
					tr1+="<td>"+rows[i].swz+"</td>";
					tr1+="<td>"+rows[i].tdz+"</td>";
					tr1+="<td>"+rows[i].bz+"</td>";
					tr1+="</tr>";
					
					$("#datagrid").append(tr1);
				}
				
				//$(this).append(tr1);
				
			}
			
		})
		
		
	}
})