$(function(){
	var client = $('.client');
	
	jQuery.each(client, function(i, val) {
		var projects = $(val).find(".projects");
		$(val).find("h2").click(function() {
			if($(this).hasClass("active"))
				$(this).removeClass("active");
			else
				$(this).addClass("active");
			projects.slideToggle("normal");
            return false;
		});
	});
	
});