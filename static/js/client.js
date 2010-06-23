$(document).ready(function () {
	var host = document.referrer;
    var protocol = (("https:" == document.location.protocol) ? "https://" : "http://");

	if (host != "") { //they typed in the URL straight away so don't have a referrer...
		var reg = /\w+:\/\//;

		host = host.replace(reg, "");
		host = host.substr(0, host.indexOf("/"));
	}
	
	$('#url_fragment').text(protocol+host+"/"+$('#id_path').val());
	$('#url_fragment').attr({
		href: protocol+host+"/"+$('#id_path').val()
	});
	$('#id_name, #id_path').keyup(function () {

		$('#url_fragment').text(protocol+host+"/"+$('#id_path').val());
	});
});

