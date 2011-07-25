function show(id_to_show, id_to_hide, choice){
	$(id_to_show).show();
	$(id_to_hide).hide();
	if (id_to_show==='#list_section')
		// pass this value to the backend with the hidden input type
	{
		document.forms.viewform.view_preference.value= 'list';
	}
	else
	{
		document.forms.viewform.view_preference.value = 'grid';
	}
	// toggle the checkbox based on whether current display equals the user's choice
	if (id_to_show==='#'+choice+'_section')
	{
		document.viewform.approved.checked = true;
		// disable the checkbox if it is currently checked
		document.viewform.approved.disabled= true;
	}
	else 
	{
		document.viewform.approved.checked = false;
		document.viewform.approved.disabled= false;
	}
	
}

function gotosection(value){
	window.location = value;
}
