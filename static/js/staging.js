/* staging javascript */
$(document).ready(function () {
	$('select.dropdown').dropdown({onchange:function(e){
		setTimeout(function(){
			document.location = e.val();
		}, 10);
	}});
    
	$('.tab').click(function(e){
		if (window.location.hash != this.hash)
			window.location.hash = this.hash;
	});

	$('#project_switcher').change(function() {
		document.location = $('#project_switcher').val();
	});

	$('#maincontent .subnav').tabs();
});

