$(document).ready(function(){
	info.message = new Message();
	init_qqFace();
	$('.suck').click(here)
});

function here(e)
{
	alert($(e.currentTarget).html());
}

function Message()
{
	var uid;
	var lid;
	var user;
	var message_view;

	var init = function()
	{
		uid = info.uid;
		lid = info.lid;
		user = info.user;
		message_view = new MessageView();
		init_uploadify();
	};
	
	var init_uploadify = function()
	{
		$('#file_upload').uploadify({
			height:	30,
			width: 120,
			swf: '/static/uploadify/uploadify.swf',
			uploader: '/lovers/home/image_upload/',
			buttonText: '上传图片',
			sizeLimit: '20240',	//kb, 20MB
			formData: {'lid': lid},
			fileTypeExts: '*.jpg;*.gif;*.png',
			onUploadSuccess: function(file, data, response) {
			// use user id to make it convienient to delete the temp image file
				$('#prepare').html("<div class='span12'><img id='temp_img" + uid + "' src='/static/pic/" + lid + "/temp_s" + uid + ".jpg' /></div>");
			}
		});
	}
	
	var Msg = Backbone.Model.extend({
		urlRoot: '/lovers/home/sendtext/',
		defaults: {
		    content: null,
		   	uid: info.uid,
			lid: info.lid,
			user: info.user 
		}
	});

	var Comment = Backbone.Model.extend({
		urlRoot: '/lovers/home/',
		defaults: {
		    content: null,
		   	uid: uid,
			mid: null,
		}
	});

	var MessageView = Backbone.View.extend({
		el: $("body"),
		initialize: function () {
		},
		events: {
			"click #submit_message":  "send_message",
		   	"click .close":  "delete_msg_or_comment",
			"click .get_comment": "get_comment",
			"click .comment": "send_comment",
			"click .img_block": "image_click"
		},

		send_message: function (e) {
			var content = $('#msg_content').val()
			var message_model = new Msg({content: content});
	
			message_model.save(null, 
				//alter the accept type in header from json to html!!!
				{ dataType: 'html',						
				success: function(model, response) {
					response = response.replace(/\[\/表情([0-9]*)\]/g,'<img src="/static/pic/face/$1.gif" border="0" />');
//					$('#message').prepend(response).fadeIn();	//add message to show
//					$(response).hide().prependTo('#message').fadeIn("slow");
					$(response).prependTo('#message').hide().slideDown("slow");
					$('#msg_content').val('');	//delete the content of input text
					mid = $('#message').children().first().attr('id');	//!!pay to here
					$('#temp_img' + uid).remove();
				},
				error: function(model, response) {
					alert(response.status);
				}
			});
		},

		delete_msg_or_comment: function(e) {
			$(e.currentTarget).parent().remove();
			var id = e.target.parentNode.id;
			var type = e.target.parentNode.className;
			if(type == 'message_info container-fluid')
			{
				var data = {'mid': id, 'lid': info.lid, 'uid': info.uid};
				var url = '/lovers/home/deletemessage/';
				ajax_delete(id, data, url);
			}
			else if(type == 'comment_content row')
			{
		//		alert(id.replace(/[^0-9]/ig, ''));
				var uid = $('#cmt' + id).attr('alt');
				var data = {'cid': id.replace(/[^0-9]/ig, ''), 'uid': info.uid};
				var url = '/lovers/home/deletecomment/';
				ajax_delete(id, data, url);
			}
		},

		get_comment: function(e)
		{	
//			var mid = e.target.parentNode.parentNode.parentNode.id;	//pay attention to this
			var mid = $(e.currentTarget).data('mid');
			var lid = $(e.currentTarget).data('lid');
			var cn = $('#gc' + mid);	//current node
//			var lid = $(e.currentTarget).data('lid');
			if(cn.attr('alt') == 'active')
			{
				$.ajax({
					type: 'POST',
					url: '/lovers/home/getcomment/' + mid + "/",
					data: {'mid': mid, 'lid': lid},
					success: function(result){
						$('#uc' + mid).hide().html(result).slideDown('slow');				//uc === user content
					},
					dataType: 'html'
				});
				cn.attr('alt', 'inactive');
			}
			else
			{
				cn.attr('alt', 'active');
				$('#uc' + mid).html('');
					
			}
		},

		send_comment: function (e)
		{
			var mid = $(e.currentTarget).data('mid');
			var lid = $(e.currentTarget).data('lid');
			var ct = $('#ct' + mid);	//ct === content text
//			var mid = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id;
			if(ct.val() != '')
			{
				uid = $('#user').attr('alt');
				content = $('#ct' + mid).val();
				$.ajax({
					type: 'POST',
					url: '/lovers/home/sendcomment/' + mid + "/",
					data: {'mid': mid, 'uid': uid, 'content': content, 'lid': lid},
					success: function(result){
//						$('#cc' + mid).prepend(result);
						$(result).hide().prependTo('#cc' + mid).slideDown('slow');
						$('#ct' + mid).val('');
					},
					dataType: 'html'
				});
			}
			else
			{
				alert('null!!');
			}
		},
		
		image_click: function (e)
		{
//			var mid = e.target.parentNode.parentNode.parentNode.parentNode.id;
			var mid = $(e.currentTarget).data('mid');
			var lid = $(e.currentTarget).data('lid');
			var img_block = $('#img' + mid);
			img_block.children().first().remove();
			if(img_block.attr('alt') == 'mid')
			{
//				img_block.prepend("<img src='/static/pic/" + lid + "/msg/" + mid + ".jpg'></img>");
				$("<img src='/static/pic/" + lid + "/msg/" + mid + ".jpg'></img>").hide().prependTo(img_block).fadeIn("slow");
				img_block.attr('alt', 'big');
			}
			else
			{
				img_block.prepend("<img src='/static/pic/" + lid + "/msg/" + mid + "m.jpg'></img>")
				img_block.attr('alt', 'mid');
			}
		}

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

function Search()
{

}

var info = 
{
	lid: $('#lovespace').attr('alt'),
	uid: $('#user').attr('alt'),
	user: $('#user').data('user'),
	message: null
}

function init_qqFace()
{
	$('#face1').qqFace({
		id : 'facebox1', //表情盒子的ID
		assign:'msg_content', //给那个控件赋值
		path:'/static/pic/face/'	//表情存放的路径
	});

	$('.message_content').each(function(){
		content = $(this).html();
		content = content.replace(/\[\/表情([0-9]*)\]/g,'<img src="/static/pic/face/$1.gif" border="0" />');
		$(this).html(content)
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
