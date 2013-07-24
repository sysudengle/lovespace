$(document).ready(function(){
	init_accept_button();
});

function init_accept_button()
{
	$('.accept').click(click_accept);
}

function click_accept(event)
{
	id = event.target.id;
	$('#lover_form').attr('action', id);
}
