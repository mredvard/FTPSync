// Main JS 
$(document).ready(function() {
	$('input.clear-default').clickClear();
	// $(".email").click(function() {
	// 		if ($(this).val() == "you@example") {
	// 			$(this).addClass('active');
	// 		}
	// 	});
	$('.notify-email-submit').attr('disabled', 'disabled');
	$('#wtf').click(function() {
		$('#error').html('');
		$(this).fadeOut();
		$('#wtf-back').fadeIn();
		$('#notify-wrapper').animate({
			opacity: 0,
			top: '15%'
			}, 1000, function() {
	 		// Animation complete.
		});
		$('#newname').animate({
			opacity: 'show',
			top: '35%'
			}, 1000, function() {
	 		// Animation complete.
		});		
	});
	$('#wtf-back').click(function() {
		$(this).fadeOut();
		$('#wtf').fadeIn();
		$('#notify-wrapper').animate({
			opacity: 1,
			top: '25%'
			}, 1000, function() {
	 		// Animation complete.
		});
		$('#newname').animate({
			opacity: 'hide',
			top: '40%'
			}, 1000, function() {
	 		// Animation complete.
		});		
	});
});

/**
 * Clears a text form element when it has the style 'clear-default'
 */
$.fn.clickClear = function() {
	return this.each(function() {
		this.defaultValue = $(this).val();
		$(this).click(function() {
			if ($(this).val() == this.defaultValue) {
				$(this).val('');
				$(this).addClass('active');
				$('.notify-email-submit').removeClass('disabled');
				$('.notify-email-submit').removeAttr('disabled');
			};
		}).focus(function() {
			if ($(this).val() == this.defaultValue) {
				$(this).val('');
				$(this).addClass('active');
				$('.notify-email-submit').removeClass('disabled');
				$('.notify-email-submit').removeAttr('disabled');
			};
		}).blur(function() {
			if ($(this).val() == "") {
				$(this).val(this.defaultValue);
				$(this).removeClass('active');
				$('.notify-email-submit').addClass('disabled');
				$('.notify-email-submit').attr('disabled', 'disabled');
			};
		});
		
		$('form').submit(function(event) {
			if ($(this).val() == this.defaultValue) {
				$(this).val('');
				$(this).removeClass('active');
				$('.notify-email-submit').addClass('disabled');
				$('.notify-email-submit').attr('disabled', 'disabled');
			};
		});
	});	
};

function notify() {
	email = $("input.email").val();
	
	// VALIDATE EMAIL ADDRESSES 
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
   	var address = $('.email').val();
   	if(reg.test(address) == false) {
       	$('#error').html('The E-Mail address is invalid');
		$('#error').fadeIn('slow');
    }
	else {
		$.ajax({
			url: "notify.php",
			data: "email=" + email,
			type: "POST",
			success: function() {
				$('#notify-email-input').fadeOut('slow');
				$('#thank-you').fadeIn('slow');
				$('#error').fadeOut('slow');
			},
			error: function() {
				alert("error");
			}
		});
	}
}