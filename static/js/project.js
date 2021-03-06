/* additional javascript functions are embedded in the project.html file */

function show(id_to_show, id_to_hide)
{
	$(id_to_show).show();
	$(id_to_hide).hide();
	}
function selectSection(value){
	VAR_CURRENT_SECTION = value;
	gotosection(value);
}
function gotosection(value)
{
	window.location.href = value;
}
// remove all the options and clear the drop down list
function removeAllOptions(selectbox)
{
	$(selectbox.children).each(function(){
		$(this).remove();
	});
}

// add one option to a drop down list
function addOption(selectbox,text,value )
{
	$(selectbox).append(
        $('<option></option>').val(value).html(text)
    );
}

// update the users preference that is stored in the database when the user switches
// between grid and list view 
function show_ajax(viewchoice, client, projectpath, id_to_show, id_to_hide)
{
	$.ajax({
			url: "/client/"+client+"/"+projectpath+"/",
			data: {choice: viewchoice},
			success: function(){
				oldChoice = VAR_CHOICE;
				VAR_CHOICE = viewchoice;
				oldSection = VAR_CURRENT_SECTION;
				$(id_to_hide).hide();
				// open the newly selected grid or list view on the category/tab that was last viewed
				gotosection('#'+VAR_CURRENT_CATEGORY);
				fillDropdown(VAR_CURRENT_CATEGORY, VAR_CHOICE);	
				$(id_to_show).show();
				// construct the jquery tools tabs
				$("ul.tabs").tabs("div.panes"+viewchoice +" > div");	
				generateClickEvents();							
				// jump to show the last viewed section unless it was the first section
				// in which case it will be visible at the top of the page automatically, no need to jump to it
				if(!(oldSection.indexOf('#1') === 0 && oldSection.charAt(2) === "_")){				
					newSection = oldSection.replace('_'+oldChoice, '_'+viewchoice);
					$('#select_section').val(newSection);
					gotosection(newSection);
					// save the oldSection because fillDropdown() has changed it
					VAR_CURRENT_SECTION = oldSection;
				}
			}
	});
}

