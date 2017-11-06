
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
            $("#see-post").attr("disabled",true);
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
                $("#save-msg").html("已发布");
                $("#publish-btn").attr("disabled",true);
                $("#see-post").attr("disabled",false);

            },
            complete:function(){

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

      $('#tail').load(url + ' #container');
    });


    $('#books a').click(function(e){
        e.preventDefault();
        var url = this.href;
        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $.get(url,function(responseText){
            dom = $(responseText)
            //var blctn = dom.find("#blctn").html();
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();
            var tag_form = dom.find("#new-tag-form").html();
            //$('#blctn').html(blctn);
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);
            $('#new-tag-form').html(tag_form);
        });

        $(this).children().addClass("select-book");
        $(this).children().css("background","#8E8E38");
        $(this).siblings().children().removeClass("select-book");
        $(this).siblings().children().css("background","#8B814C");
    });

    $('#tags a').click(function(e){
        e.preventDefault();
        var url = this.href;

        if(history.pushState){
            var state=({
              url: url, title:''
             });
             window.history.pushState(state, '', url);
        }
        else
        {
           window.location.href=url;
        }

        $('#plctn').remove();
        $('#post-list').load(url + ' #plctn');

        $(this).children().addClass("select-tag");
        $(this).children().css("background","#F0E68C");
        $(this).siblings().children().removeClass("select-tag");
        $(this).siblings().children().css("background","#F5FFFA");
    });


    $('#nbf').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        success:function(responseText)
        {
            var url = $('#nbf').attr('action');
            if(history.pushState){
                var state=({
                  url: url, title:''
                 });
                 window.history.pushState(state, '', url);
            }

            dom = $(responseText)
            var blctn = dom.find("#blctn").html();
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();

            $('#blctn').html(blctn);
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);

            $("#id_book_name").val("");
            $('#new-book-form').hide(200);
        }
        });
        return false;
    });

   $('#ntf').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        success:function(responseText)
        {
            var url = $('#ntf').attr('action');
            if(history.pushState){
                var state=({
                  url: url, title:''
                 });
                 window.history.pushState(state, '', url);
            }

            dom = $(responseText)
            var tlctn = dom.find("#tlctn").html();
            var plctn = dom.find("#plctn").html();
            $('#tlctn').html(tlctn);
            $('#plctn').html(plctn);

            $("#id_tag_name").val("");
            $('#new-tag-form').hide(200);
        }
        });
        return false;
    });


});

$(document).bind('input propertychange', function(){
        $("#save-msg").html("未保存");
        $("#publish-btn").attr("disabled",false);
        $("#save-btn").attr("disabled",false);
   });


