$(document).ready(mainfunction);

function mainfunction () {
	$("a.photo").click(showPhoto);
}

function showPhoto () {
    var photoId = $(this).attr("class").split(" ")[1].toString();
    var c = "div." + photoId;
    $("div.active").removeClass("active");
    $(c).addClass("active");
}
