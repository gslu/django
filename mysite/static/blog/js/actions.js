
$(document).ready(function() {


    $("#back-top").click(function() {
                      $("body,html").animate({scrollTop:0}, 200);
                      return false;
                  });


// 使用 jQuery异步提交表单

    $('#write-form').submit(function() {
        jQuery.ajax({
        url:this.action,
        data:$(this).serialize(),
        type:this.method,
        dataType:"html",
        beforeSend:function()
        {
            $("#save-msg").text("正在保存..");
        },
        success:function(responseText)
        {
            $("#save-msg").text("已保存");
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
            success:function(responseText)
            {
                $("#save-msg").text("已保存");
                $("#save-btn").attr("disabled",true);
                $("#save-msg").text("已发布");
                $("#publish-btn").attr("disabled",true);
                $("#see-post").attr("disabled",false);
                dom = $(responseText);
                $("#see-post").attr("onclick",dom.find("#see-post").attr("onclick"));
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

          $("#tail").html($(response).find("#tail").html());
          $(".column-bar").html($(response).filter(".column-bar").html());
         });

      $('#container').remove();
      $('.nav-ul a').css("color",'#424242');
      $('.'+cls).css("color",'#CD2626');
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



   $('#id_image').change(function(){
        var file = this.files[0];
        name = file.name;
        size = file.size;
        type = file.type;
        //your validation

        $("#image-form").ajaxSubmit({
            dataType :'json',//返回数据类型
            beforeSend:function(){
                $("#change-image").text("正在上传..");
            },
            success:function(data){
                $("#change-image").text("变更头像");
                if(data.path != "error")
                {
                    $('.user-image img').attr("src",data.path);
                    $("#save-status").text("成功变更头像")
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);
                }
                else
                {alert("系统异常！");}
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });

   $('#id_bgimg').change(function(){
        var file = this.files[0];
        name = file.name;
        size = file.size;
        type = file.type;
        //your validation

        $("#bgimg-form").ajaxSubmit({
            dataType :'json',//返回数据类型
            beforeSend:function(){
                $("#change-bgimg").text("正在上传..");
            },
            success:function(data){
                $("#change-bgimg").text("变更背景");
                if(data.path != "error")
                {
                    $('.bg-image img').attr("src",data.path);
                    $("#save-status").text("成功变更背景")
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);
                }
                else
                {alert("系统异常！");}
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });


    $("#save-setting").click(function(){
        $("#bpc-form").ajaxSubmit({
            dataType :'json',//返回数据类型
            beforeSend:function(){

            },
            success:function(data){

                if(data.path != "error")
                {
                    $("#save-status").text("成功保存设置")
                    $("#save-status").slideToggle(800);
                    $("#save-status").slideToggle(1200);
                }
                else
                {alert("系统异常！");}
            },
            error:function(xhr){
                alert("上传失败！");
            }
        });
    });

});



