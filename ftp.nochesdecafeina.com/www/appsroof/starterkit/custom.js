jQuery(document).ready(function() {
	// do something here
	$("#orderedlist li:last").hover( function(){
			$(this).addClass("green");
		},function(){
			$(this).removeClass("green");
	});
	$("#orderedlist").find("li").each(function(i) {
    	$(this).append(" BAM " + i);
    });
	
	$("#reset").click(function() {
        $("form").each(function(i) {
           this.reset(); 
        });
    });
	
	$("li").filter(":has(ul)").css("border","1px solid black");
	
	$("a[name='bottom']").css("background", "#eee");
	
	$('#faq').find('dd').hide().end().find('dt').click(function() {
     	$(this).next().fadeToggle();
   });
});