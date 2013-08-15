$(document).ready(function(){
	init_send_magicword_button();
	init_close_button();
});

function init_send_magicword_button()
{
	$('#submit_magicword').click(submit_magicword_by_ajax);
}

function init_close_button()
{
	$('.close').click(close_click);
}

function submit_magicword_by_ajax()
{
	content = $('#magicword_input').val()
	user = $('#user').data('user');
	uid = $('#user').attr('alt')
	lid = $('#lovespace').attr('alt')
	$.ajax({
		type: 'POST',
		url: '/lovers/magic/sendtext/',
		data: {'content': content, 'uid': uid, 'lid': lid, 'user': user},
		success: function(result){
			$('#magicword').prepend(result);	//add magicword to show
			$('#magicword_input').val('');	//delete the content of input text
			$('.close').click(close_click);
		},
		dataType: 'html'
	});
}

function close_click(event)
{
	var id = event.target.parentNode.id;
	var uid = $('#' + id).attr('alt');
	var lid = $('#lovespace').attr('alt');
	var data = {'mid': id.replace(/[^0-9]/ig, ''), 'lid': lid, 'uid': uid};
	var url = '/lovers/magic/deletemagicword/';
	ajax_delete(id, data, url);
}

function ajax_delete(id, Data, Url)
{
	$.ajax({
		type: 'POST',
		url: Url,
		data: Data,
		success: function(result){
			$('#' + id).remove();
		},
		dataType: 'html'
	});
}
//this is from django website
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
