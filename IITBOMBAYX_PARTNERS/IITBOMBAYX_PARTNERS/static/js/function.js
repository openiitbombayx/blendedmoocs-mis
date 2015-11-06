$(function(){

	function Edit(){
		var par = $(this).parent().parent(); //tr
		var tdrollno = par.children("td:nth-child(1)");
		var tdusername = par.children("td:nth-child(2)");
		var tdEmail = par.children("td:nth-child(3)");
		var tdBtn = par.children("td:nth-child(4)");

		tdrollno.html("<input type='text' name='h1' id='txtNome' value='"+tdrollno.html()+"'/>");
		tdusername.html("<input type='text' name='h2' id='txtTelefone' value='"+tdusername.html()+"'/>");
		tdEmail.html("<input type='text' name='h3' id='txtEmail' value='"+tdEmail.html()+"'/>");
		tdBtn.html("<button class='btnSave' type='submit' >submit</button>");

		$(".btnSave").bind("click", Save);
		$(".btnEdit").bind("click", Edit);
	};

	function Save(){
		var par = $(this).parent().parent(); //tr
		var tdrollno = par.children("td:nth-child(1)");
		var tdusername = par.children("td:nth-child(2)");
		var tdEmail = par.children("td:nth-child(3)");
		var tdBtn = par.children("td:nth-child(4)");

		tdrollno.html(tdrollno.children("input[type=text]").val());
		tdusername.html(tdusername.children("input[type=text]").val());
		tdEmail.html(tdEmail.children("input[type=text]").val());
		tdBtn.html("<img src='images/pencil.png' class='btnEdit'/>");

		$(".btnEdit").bind("click", Edit);
	};

	$(".btnEdit").bind("click", Edit);		

});
