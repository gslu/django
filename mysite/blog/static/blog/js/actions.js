
$(document).ready(function() {

// 使用 jQuery异步提交表单

    $('#write-form').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        beforeSend:function()
        {
            $("#save-msg").html("正在保存..");
        },
        success:function()
        {
            $("#save-msg").html("已保存");
            $("#save-btn").attr("disabled",true);
        }
        });
        return false;
        });

    $("#write-form :input").change(function(){ $("#save-msg").html("未保存"); });


    $('#publish-btn').click(function(){
            jQuery.ajax({
            url:"./publish/",
            data:$("#write-form").serialize(),
            type:"POST",
            beforeSend:function()
            {
                $("#save-msg").html("正在保存..");
            },
            success:function()
            {
                $("#save-msg").html("已保存");
                $("#save-btn").attr("disabled",true);

            },
            complete:function(){
                $("#save-msg").html("已发布");
                $("#publish-btn").attr("disabled",true);

            },
            });
            return false;
     });

    $('.nav-ul a').on('click', function(e) {
      e.preventDefault();  // 阻止链接跳转
      var url = this.href;  // 保存点击的地址
      var cls = $(this).attr('class');

      $.get(url,function(response){
          var newtitle = $(response).filter("title").text();
          document.title = newtitle;
          if(history.pushState){
              var state=({
                url: url, title:newtitle
                });
              window.history.pushState(state, newtitle, url);
          }
          else
          {
            window.location.href=url;
          }
          });
      $('#container').remove();
      $('.nav-ul a').css("color",'#5E5E5E')
      $('.'+cls).css("color",'#8B2500');
      $('#tail').load(url + ' #container'); // 加载新内容,url地址与该地址下的选择器之间要有空格,表示该url下的#container
    });

});

$(document).bind('input propertychange', function(){
        $("#save-msg").html("未保存");
        $("#publish-btn").attr("disabled",false);
        $("#save-btn").attr("disabled",false);

   });
