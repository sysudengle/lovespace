$(document).ready(function(){
	info.message = new Search();
});

function Search()
{
	var concern_view;
	
	var init = function()
	{
		concern_view = new ConcernView();
	}

	var Concern = Backbone.Model.extend({
//		urlRoot: '/lovers/add_concern/',
		defaults: {
		   	uid: info.uid,
			tid: null
		},
		methodToURL: {
			'create': '/lovers/add_concern/',
			'delete': '/lovers/delete_concern/'
		},
		sync: function(method, model, options) {
			options = options || {};
			options.url = model.methodToURL[method.toLowerCase()];

			Backbone.sync(method, model, options);
		}
	});
	var ConcernView = Backbone.View.extend({
		el: $("body"),
		initialize: function () {
		},
		events: {
			"click .concern": "add_concern",
			"click .cancel_concern": "cancel_concern"
		},
		add_concern: function(e) {
			var btn = $(e.currentTarget);
			var lid = btn.attr('alt');
			var concern = new Concern({tid: lid});

			concern.save(null,
				{ dataType: 'html',
					success: function(model, response)
					{
						btn.attr('class', 'cancel_concern btn btn-danger');
						btn.html('取消关注');
					},
					error: function(model, response)
					{
						alert('failure');
					}
				}
			);
		},
		cancel_concern: function(e) {
			var btn = $(e.currentTarget);
			var lid = btn.attr('alt');

			$.ajax({
				type: 'POST',
				url: '/lovers/delete_concern/',
				data: {'uid': info.uid, 'tid': lid},
				success: function(result){
					btn.attr('class', 'concern btn btn-primary');
					btn.html('关注');
				},
				error: function(result) {
					alert('fail~cancel');
				},
				dataType: 'html'
			});

		}
	});
	init();
}

var info = 
{
	lid: $('#lovespace').attr('alt'),
	uid: $('#user').attr('alt'),
	user: $('#user').html(),
	search: null
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
