$(document).ready(function(){
	init_accept_button();
	init_refuse_button();
    $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd'});
});

function init_accept_button()
{
	$('.accept').click(click_accept);
}

function click_accept(e)
{
	id = e.target.id;
	$('#lover_form').attr('action', id);
}

function init_refuse_button()
{
	$('.refuse').click(refuse_request);
}

function refuse_request(e)
{
	var fid = $(e.currentTarget).data('fid');
	var tid = $(e.currentTarget).data('tid');
	$.ajax({
		type: 'POST',
		url: '/' + fid + '/user/refuselover/' + tid + '/',
		success: function(result){
			$('#invite' + tid).remove();
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
