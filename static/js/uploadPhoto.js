$(document).ready(function(){
	info.album = new Album();
});

var info = 
{
	lid: $('#lovespace').attr('alt'),
	uid: $('#user').attr('alt'),
	album: null
}

function Album()
{
	var uid;
	var lid;
	var album_view;
	var aid;

	var init = function()
	{
		uid = info.uid;
		lid = info.lid;
		aid = location.toString().split('/')[6];
		album_view = new AlbumView();
		init_uploadify();
	};
	
	var init_uploadify = function()
	{
		$('#photoName').uploadify({
			height:	30,
			width: 100,
			swf: '/static/uploadify/uploadify.swf',
			uploader: '/lovers/photo/uploadphoto/',
			buttonText: '添加图片',
			sizeLimit: '20240',	//kb, 20MB
			fileTypeExts: '*.jpg;*.gif;*.png;*.jpeg;*.JPEG;*.JPG;*.GIF;*.PNG',
			formData: {'lid': lid,'aid': aid},
			onUploadSuccess: function(file, data, response) {
				var pname = data;
				$("#upload").append("<div class='float'><button type='button' class='close'> <i class='icon-remove-sign'></i> </button><a class='fancybox' data-fancybox-group='gallery' href='/static/pic/" + lid + "/" + aid + "/" + pname + "'><img src='/static/pic/" + lid + "/" + aid + "/c" + pname + "' alt='' /></a></div>");
			}
		});
	}

	var AlbumView = Backbone.View.extend({
		el: $("body"),
		initialize: function () {
		},
		events: {
		   	"click .close":  "delete_album_or_photo",
		},

		delete_album_or_photo: function(e) {
			$(e.currentTarget).parent().remove();
			var id = e.target.parentNode.parentNode.id;
			var type = e.target.parentNode.parentNode.className;
			if(type == 'thumbnail albumblock')
			{
				var data = {'aid': id, 'lid': info.lid, 'uid': info.uid};
				var url = '/lovers/album/deletealbum/';
				ajax_delete(id, data, url);
			}
			else if(type == 'float')
			{
				var data = {'aid': aid, 'photo_name': id, 'lid': info.lid, 'uid': info.uid};
				var url = '/lovers/album/deletephoto/';
				ajax_delete(id, data, url);
		//		alert(id.replace(/[^0-9]/ig, ''));
				// var uid = $('#cmt' + id).attr('alt');
				// var data = {'cid': id.replace(/[^0-9]/ig, ''), 'uid': uid};
				// var url = '/lovers/home/deletecomment/';
				// ajax_delete(id, data, url);
			}
		},
	});

	var ajax_delete = function(id, Data, Url)
	{
		$.ajax({
			type: 'POST',
			url: Url,
			data: Data,
			success: function(result){
//				$('#' + id).slideUp('slow', function() { alert('fuck'); $(this).remove();});
				$('#' + id).slideUp('slow');
			},
			dataType: 'html'
		});
	};

	init();
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
