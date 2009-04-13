$(document).ready(function() {
	
	if(document.location.search == "?m=nav") {
		$("#nav .wrap").css("top","0");
	}	


	$("#nav").hover(
		function() {
		$("#nav .wrap").animate({
				top: "0"
			}, "normal", "swing");
		},
		function() {
			$("#nav .wrap").animate({
				top: "-63px"
			}, "slow", "swing");
		}
	);
	
});