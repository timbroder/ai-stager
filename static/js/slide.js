$(document).ready(function() {
	if(document.location.search == "?m=nav") {
		$("#nav .wrap").css("top","0");
	}
	
	$("#nav").hoverIntent({
		over: function() { $("#nav .wrap").animate({ top: "0"}, 250, "swing"); },
		out:  function() { $("#nav .wrap").animate({ top: "-63px" }, 200, "swing"); },
		sensitivity: 7,
		interval: 500,
		timeout:  300
	});
});