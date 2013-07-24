$(document).ready(function() {
    $('#photoName').uploadify({
        'swf': '/static/uploadify/uploadify.swf',
        'uploader' : '',
        'buttonClass': 'btn btn-info',
        'removeCompleted': true,
        'removeTimeout': 0,
        'fileTypeExts': '*.jpg;*.gif;*.png;*.jpeg;*.JPEG;*.JPG;*.GIF;*.PNG',
        'multi': true,
        'fileSizeLimit': 20*1024*1024,
        'buttonText': '添加图片',
        // 'formData': {
        //     'tmp_folder': '{{ flag }}',
        //     'user_id': '{{ loginuser.id }}',
        // },
        'onUploadSuccess': function(file, data, response) {
            var lid = location.toString().split('/')[5];
            var aid = location.toString().split('/')[6];
            var pid = data.split(" ")[0];
            var pname = data.split(" ")[1];
            $("#upload").append("<li class='span2'><div><a class='photo " + pid + "' href='#modalPhoto' role='button' data-toggle='modal'><img class='img-rounded' src='/static/pic/" + lid + "/" + aid +"/c" + pname +"'/> </a></div></li>");
        },
    });
});
