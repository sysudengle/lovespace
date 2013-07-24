$(document).ready(function(){
	init_send_msg_button();
	init_get_comment_href();
	init_image();
	init_uploadify();
	init_close_button();
	init_backbone();
	var dl = $('#shit').attr('alt');
	var b = Backbone.View.extend({ el: 'body'});
	a = new b();

});

function init_send_msg_button()
{
	$('#submit_message').click(submit_message_by_ajax);
}

function init_get_comment_href()
{
	$('.get_comment').click(get_comment_by_ajax);
}

function init_uploadify()
{
	var lid = $('#lovespace').attr('alt');
	var uid = $('#user').attr('alt');
	$('#file_upload').uploadify({
		height:	30,
		width: 120,
		swf: '/static/uploadify/uploadify.swf',
		uploader: '/lovers/home/image_upload/',
		buttonText: 'upload',
		sizeLimit: '20240',	//kb, 20MB
		formData: {'lid': lid},
		fileTypeExts: '*.jpg;*.gif;*.png',
		onUploadSuccess: function(file, data, response) {
			// use user id to make it convienient to delete the temp image file
			$('#db').after("<img id='temp_img" + uid + "' src='/static/pic/" + lid + "/temp_s" + uid + ".jpg' />");
		}
	});
}

function init_image()
{
	$('.img_block').click(img_click);
}

function init_close_button()
{
	$('.close').click(close_click);
}

function submit_message_by_ajax()
{
	var user = $('#user').html()
	var uid = $('#user').attr('alt')
	var lid = $('#lovespace').attr('alt')
	$.ajax({
		type: 'POST',
		url: '/lovers/home/sendtext/',
		data: {'content': content, 'uid': uid, 'lid': lid, 'user': user},
		success: function(result){
			$('#message').prepend(result);	//add message to show
			$('#msg_content').val('');	//delete the content of input text
			mid = $('#message').children().first().attr('id');	//!!pay to here
			$('#gc' + mid).click(get_comment_by_ajax);	//gc === get comment
			$('#temp_img' + uid).remove();
			$('#img' + mid).click(img_click);
			$('.close').click(close_click);
		},
		dataType: 'html'
	});
}

function get_comment_by_ajax(event)
{
	var mid = event.target.parentNode.parentNode.id;	//pay attention to this
	var cn = $('#gc' + mid);	//current node
	if(cn.attr('alt') == 'active')
	{
	//	alert('/lovers/home/getcomment/' + mid + "/");
		$.ajax({
			type: 'POST',
			url: '/lovers/home/getcomment/' + mid + "/",
			data: {'mid': mid},
			success: function(result){
				$('#uc' + mid).html(result);				//uc === user content
				$('#sc' + mid).click(send_comment_by_ajax);	//sc === send content
				$('.close').click(close_click);
			},
			dataType: 'html'
		});
		//event.target.setAttribute('alt', 'inactive');
		cn.attr('alt', 'inactive');
	}
	else
	{
		cn.attr('alt', 'active');
//		event.target.parentNode.nextSibling.nextSibling.innerHTML = '';	//pay attention to \n, it is also a node
		$('#uc' + mid).html('');
	}
}

function send_comment_by_ajax(event)
{
	var mid = event.target.parentNode.parentNode.parentNode.parentNode.parentNode.id;
	var ct = $('#ct' + mid);	//ct === content text
	if(ct.val() != '')
	{
		uid = $('#user').attr('alt');
		content = $('#ct' + mid).val();
		$.ajax({
			type: 'POST',
			url: '/lovers/home/sendcomment/' + mid + "/",
			data: {'mid': mid, 'uid': uid, 'content': content},
			success: function(result){
				$('#cc' + mid).prepend(result);
				$('#ct' + mid).val('');
				$('.close').click(close_click);
			},
			dataType: 'html'
		});
	}
	else
	{
		alert("not null!!");
	}

}

function img_click(event)
{
	var mid = event.target.parentNode.parentNode.parentNode.id;
	var lid = $('#lovespace').attr('alt')
	var img_block = $('#img' + mid);
	img_block.children().first().remove();
	if(img_block.attr('alt') == 'mid')
	{
		img_block.prepend("<img src='/static/pic/" + lid + "/msg/" + mid + ".jpg'></img>");
		img_block.attr('alt', 'big');
	}
	else
	{
		img_block.prepend("<img src='/static/pic/" + lid + "/msg/" + mid + "m.jpg'></img>")
		img_block.attr('alt', 'mid');
	}
}

function close_click(event)
{
	var id = event.target.parentNode.id;
	var type = event.target.parentNode.className;
	if(type == 'message_info')
	{
		var uid = $('#' + id).attr('alt');
		var lid = $('#lovespace').attr('alt');
		var data = {'mid': id, 'lid': lid, 'uid': uid};
		var url = '/lovers/home/deletemessage/';
		ajax_delete(id, data, url);
	}
	else if(type == 'comment_content')
	{
//		alert(id.replace(/[^0-9]/ig, ''));
		var uid = $('#cmt' + id).attr('alt');
		var data = {'cid': id.replace(/[^0-9]/ig, ''), 'uid': uid};
		var url = '/lovers/home/deletecomment/';
		ajax_delete(id, data, url);
	}
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

function init_backbone()
{
	Friend = Backbone.Model.extend({
		urlRoot: '/lovers/home/sendtext/',
		defaults: {
		    name: null,
		   	psw: null
		}
	});

	Friends = Backbone.Collection.extend({
		    initialize: function (options) {
				        this.bind("add", options.view.addFriendList);
						    }
	});
	window.AppView = Backbone.View.extend({
		        el: $("body"),
		        initialize: function () {
					            this.friends = new Friends({ view: this });
								        },
		        events: {
					            "click #add-friend":  "showPrompt",
		            "click .delete":  "delete_li"
		        },
		        delete_li: function(e) {
					            $(e.currentTarget).parent().remove();
								        },
		        showPrompt: function () {
					            var username = $("input[name=username]").val() || "";
								this.friend_model = new Friend({name: username, psw: 1});
//								this.friend_model.save(JSON.stringify(this.friend_model));
								this.friend_model.save(null, {
									success: function() {
										;
									},
									error: function(model, response) {
										alert('fuck');
									}
								});
								this.friends.add(this.friend_model);
								alert(this.friends);
														        },
		        addFriendList: function (model) {
					            $("#friends-list").append("<li style='margin-top:5px;'>Friend name: " + model.get('name') + " <button class='btn btn-danger delete'>Delete Friend</button></li>");
								        }
	    });
	var appview = new AppView;
}

function handler1(model, response)
{
	alert(text);
}

function handler2(model, response)
{
	alert(text);
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
