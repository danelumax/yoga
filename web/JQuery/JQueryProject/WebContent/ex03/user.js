$().ready(function(){
	var index = 1;
	/**
	 * 完成添加功能
	 */
	$("#addUser").click(function(){
		/**
		 * 1、获取姓名,电话,email的值
		 * 2、创建
		 *     <tr>
		 *         <td><input type="checkbox"></td>
		 *         <td>${姓名}</td>
		 *         <td>${email}</td>
		 *         <td>${phone}</td>
		 *         <td><a>修改</a></td>
		 *         <td><a>删除</a></td>
		 *     </tr>
		 * 3、把创建完成的tr追加到tbody上
		 */
		var name = $("#name").val();
		var email = $("#email").val();
		var tel = $("#tel").val();
		
		var $checkbox = $("<input/>").attr("type","checkbox");
		var $checkboxTD = $("<td/>").append($checkbox);
		$checkboxTD.attr("id",index);
		index++;
		
		var $nameTD = $("<td/>").text(name);
		
		var $emailTD = $("<td/>").text(email);
		
		var $phoneTD = $("<td/>").text(tel);
		
		var $updateA = $("<a/>").text("修改");
		/**
		 * 完成修改的功能
		 */
		$updateA.css("cursor","pointer");
		/**
		 * 给修改的超级链接添加click事件
		 */
		$updateA.click(function(){
			var name = $(this).parent().siblings("td:eq(1)").text();
			var email = $(this).parent().siblings("td:eq(2)").text();
			var tel = $(this).parent().siblings("td:eq(3)").text();
			var id = $(this).parent().siblings("td:eq(0)").attr("id");
			
			$("#name_update").val(name);
			$("#email_update").val(email);
			$("#tel_update").val(tel);
			$("#id_update").val(id);
		});
		var $updateTD = $("<td/>").append($updateA);
		
		var $delA = $("<a/>").text("删除");
		$delA.css("cursor","pointer");
		
		$delA.click(function(){//完成删除本行的功能
			if(window.confirm("您确认要删除吗?")){
				$(this).parent().parent().remove();	
			}
		});
		
		var $delTD = $("<td/>").append($delA);
		
		//添加 完成
		var $tr = $("<tr/>").append($checkboxTD).
			append($nameTD).append($emailTD).
			append($phoneTD)
			.append($delTD).append($updateTD);
			
		$("#usertable tbody").append($tr);
	});
	
	/**
	 * 完成删除几行的功能
	 */
	$("#deleteUser").click(function(){
		if(window.confirm("您确认要删除吗?")){
			/**
			 * :checkbox  所有的checkbox
			 *    :not(#allCheckbox) 不包含id为allCheckbox
			 *        被选中的
			 */
			$(":checkbox:not(#allCheckbox):checked").parent().parent().remove();		
		}
	});
	
	/**
	 * 全选功能
	 */
	$("#allCheckbox").click(function(){
		if($(this).attr("checked")){
			$(":checkbox:not(#allCheckbox)").attr("checked",true);
		}else{
			$(":checkbox:not(#allCheckbox)").attr("checked",false);
		}
	});
	
	/**
	 * 完成修改操作
	 */
	$("#updateUser").click(function(){
		/**
		 * 获取到修改的id的值，根据值去匹配table中的行
		 */
		var idValue = $("#id_update").val();
		var name_update = $("#name_update").val();
		var email_update = $("#email_update").val();
		var tel_update = $("#tel_update").val();
		/**
		 * 根据修改的id的值就定位某一行(td)
		 */
		$("td[id="+idValue+"]").siblings("td:eq(0)").text(name_update);
		$("td[id="+idValue+"]").siblings("td:eq(1)").text(email_update);
		$("td[id="+idValue+"]").siblings("td:eq(2)").text(tel_update);
	});
});
	