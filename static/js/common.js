function goTop(acceleration, time) {
	acceleration = acceleration || 0.1;
	time = time || 16;
 
	var x1 = 0;
	var y1 = 0;
	var x2 = 0;
	var y2 = 0;
	var x3 = 0;
	var y3 = 0;
 
	if (document.documentElement) {
		x1 = document.documentElement.scrollLeft || 0;
		y1 = document.documentElement.scrollTop || 0;
	}
	if (document.body) {
		x2 = document.body.scrollLeft || 0;
		y2 = document.body.scrollTop || 0;
	}
	var x3 = window.scrollX || 0;
	var y3 = window.scrollY || 0;
 
	// 滚动条到页面顶部的水平距离
	var x = Math.max(x1, Math.max(x2, x3));
	// 滚动条到页面顶部的垂直距离
	var y = Math.max(y1, Math.max(y2, y3));
 
	// 滚动距离 = 目前距离 / 速度, 因为距离原来越小, 速度是大于 1 的数, 所以滚动距离会越来越小
	var speed = 1 + acceleration;
	window.scrollTo(Math.floor(x / speed), Math.floor(y / speed));
 
	// 如果距离不为零, 继续调用迭代本函数
	if(x > 0 || y > 0) {
		var invokeFunction = "goTop(" + acceleration + ", " + time + ")";
		window.setTimeout(invokeFunction, time);
	}
}
$(function(){
  // 给 window 对象绑定 scroll 事件
  $(window).bind("scroll", function(){

      // 获取网页文档对象滚动条的垂直偏移
      var scrollTopNum = $(document).scrollTop(),
          // 获取浏览器当前窗口的高度
          winHeight = $(window).height(),
          returnTop = $("div.returnTop");

      // 滚动条的垂直偏移大于 0 时显示，反之隐藏
      (scrollTopNum > 0) ? returnTop.fadeIn("fast") : returnTop.fadeOut("fast");

      // 给 IE6 定位
      if (!-[1,]&&!window.XMLHttpRequest) {
          returnTop.css("top", scrollTopNum + winHeight - 200);
      }

  });

  // 点击按钮后，滚动条的垂直方向的值逐渐变为0，也就是滑动向上的效果
  $("div.returnTop").click(function() {
      $("html, body").animate({ scrollTop: 0 }, 300);
  });

});
