// JavaScript Document

$(document).ready(function() {
	$(".email").focus(function(){
		$(this).val("");
	});
	$(".email").blur(function(){
		if ($(this).val() == "") {
			$(this).val("your@email.here");	
		}
	});
});

function signup() {
	var regexp = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	var correo = $(".email").val();
	if ((regexp.test(correo) == false) || (correo == "your@email.here")) {
		alert("Invalid email!");	
	}
	else {
		$.ajax({
			url: "correos.php",
			data: "email=" + correo,
			type: "POST",
			success: function() {
				$(".textbox").fadeOut('slow');
				$(".thanks").fadeIn('slow');
			},
			error: function() {
				alert("error");
			}
		});
	}
}