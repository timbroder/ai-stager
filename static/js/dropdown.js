//Replaces option inputs with <ul><li> structures so they can by styled.

$(function($){
    $.fn.dropdown = function(options){
		options = $.extend({duration:60},options || {});
		$(this).each(function(){
			// widget functions
			var open = function(){
				styled.find('.options').slideDown(options.duration, function(){
					$(document).one('click', close);
				});	
			};
			
			var close = function(){
				styled.find('.options').hide();
			};
			
			var select = function(item, bypassEvent){
				selected.text(item.text());
				hidden.val(item.data('value'));
				
				styled.find('.options').hide()
					.find('li:hidden').show();
				item.hide();
				
				if (!bypassEvent){
					if (options.onchange){
						options.onchange(hidden, this);			
					}
		            if (handler && handler.split)
						(function(){eval(handler)}).apply(hidden.get(0));
				}
			};
			
			//build replacement
	        var orig = $(this);
			var selected = $('<a href="javascript:;" class="curSelection"></a>').click(open);
	        var styled = $('<div><input type="hidden"/><ul id="projects"><li class="default"><h4></h4><ul class="options"></ul></li></ul></div>');
			styled.find('h4').append(selected);
			var hidden = styled.find('input[type=hidden]').attr('name',orig.attr('name')).attr("class", orig.attr('class'));
			var handler = orig.attr('onchange'); // || orig.data('events')['change'];
			
			$('option', orig).each(function(i, e){
	        	var item = $('<li><a href="javascript:;">'+e.innerHTML+'</a></li>').data('value', $(e).val());
	        	item.click(function(){select(item);});
	            styled.find('.options').append(item);
	        });
			// swap
			orig.replaceWith(styled);
			select.apply(this, [styled.find('ul.options li').eq(this.selectedIndex), true]);
		});
    };	
});
